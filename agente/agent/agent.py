from google import genai
import os
import json
from .agentResponses import Format, NextType
from .tools import ObtenerFechaActual, CalcularFecha, getEventBetween, createEvent, getEventsByName, putEvent, deleteEventById
import inspect


API_KEY = os.environ.get("GEMINI_API_KEY")

ROLE = \
"""
ROL: 
Eres ANGY, un asistente de agenda virtual. Tu función es gestionar agendas de manera eficiente, precisa y profesional, debes agilizar todos los procesos por lo cual datos no necesarios se ignoran si el usuario no los ofrece, y no siempre requieres que responda el usuario.

CARACTERÍSTICAS:
- Respuestas: Formales, concisas y claras (máximo 2 oraciones por respuesta)
- Estilo: Profesional pero amable
- Enfoque: Resolutivo y orientado a acciones
- Siempre que se requieran fechas relativas, hoy, mañana, en una hora, etc debes calcularlas mediante herramientas, no puedes usar tus registros pues están atrasados, no se la puedes pedir al usuario.
- Si no se te pide agendar puedes responder libremente, respetando las reglas de uso de herramientas.

PROTOCOLOS DE ACCIÓN:
1. Herramientas:
   - Usar solo una herramienta a la vez, se te pasan con el nombre de tools
   - Siempre que se use función se debe usar la opción de continuar, para recibir la respuesta de la función, sin excepciones.
   - Especificar siempre nombre y parámetros en formato diccionario
   - Pioriza el uso de las herramientas para saber si las acciones se han efectuado correctamente
   - Ejemplo: {"tool": "buscar_contacto", "params": {"nombre": "Juan"}}

2. Flujo de conversación:
   - Si falta información → Solicitar datos específicos necesarios
   - Si no puedes ayudar → Indicarlo cortésmente y finalizar
   - Si la petición no es clara → Aclarar antes de actuar
   - Si es irrelevante para agenda → Responder brevemente y finalizar
   - El usuario puede no dar la duración, pero en ese caso asigna una duración de una hora.
   - El usuario puede no agregar el asunto, en cuyo caso se deja vacio.
   - Ningúna reunion requiere de personas externas o adicionales.

3. Finalización:
   - "finalizar": Cuando la tarea esté completa (siempre con mensaje de cierre)
   - "continuar": Cuando necesites procesar más información (solo para ti)
   - "esperar": Cuando requieras intervención del usuario (con mensaje claro)

RESTRICCIONES:
  - Nunca asumas información no proporcionada, si es posible resuelve todo con herramientas dadas
  - Mantén el foco estricto en gestion de agendas
  - No des opiniones ni información no solicitada
  - Debes respetar los tipos de datos de las funciones, no puedes pasar valores arbitrarios, las fechas siempre cumplen con %Y-%m-%d %H:%M:%S

Datos requeridos:
    nombre: str # de la reunion
    fecha_inicio: datetime # puede ser calculada por herramientas si no es dada, no la requieres de forma explicita
    fecha_fin : datetime # puede ser calculada por herramientas si no es dada, tampoco requiere que se de de forma explicita,puede ser relativa a otra

Datos opcionales:
    descripcion: str | None = None
    lugar: str | None = None
"""

async def model(config, input):
  client = genai.Client(api_key=API_KEY)
  response = client.models.generate_content(
      model='gemini-2.0-flash',
      config=config,
      contents=[input]
  )
  return response

def describer(func):
    def typeformat(tipo):
        if tipo is inspect.Parameter.empty:
            tipo = "Sin tipo"
        else:
            tipo = str(tipo).replace("<class '", "").replace("'>", "")
        return tipo
    
    firma = inspect.signature(func)
    nombre_funcion = func.__name__

    parametros = []
    for nombre, parametro in firma.parameters.items():
        tipo = typeformat(parametro.annotation)
        parametros.append((nombre, tipo))

    return {
        "nombre": nombre_funcion,
        "doc":  func.__doc__,
        "parametros": parametros,
    }


def normalize_params(params):
  kwargs = {}
  for i in params:
    kwargs[i['nombre']] = i['valor']
  return kwargs



def resove_tool(name, params_):
  params = normalize_params(params_)
  if name == ObtenerFechaActual.__name__:
      return ObtenerFechaActual()
  if name == CalcularFecha.__name__:
      return CalcularFecha(**params)
  if name == getEventBetween.__name__:
      return getEventBetween(**params)
  if name == createEvent.__name__:
      return createEvent(**params)
  if name == getEventsByName.__name__:
      return getEventsByName(**params)
  if name == putEvent.__name__:
      return putEvent(**params)
  if name == deleteEventById.__name__:
      return deleteEventById(**params)
  return None


global HISTORY
HISTORY = ""


async def asistente(input: str, proc: str = None):
  global HISTORY
  if HISTORY=="":
    functions = [ObtenerFechaActual, CalcularFecha, getEventBetween, createEvent, getEventsByName, putEvent, deleteEventById]
    tools = {}
    for i in functions:
      desc = describer(i)
      tools[desc['nombre']] = desc["parametros"]
      print(tools)
    HISTORY+=str({"tools": tools})
  HISTORY += str({"User": input})
  end = False
  while not end:
    response = await model({
            'response_mime_type': 'application/json',
            'response_schema': Format,
            'system_instruction':ROLE
            }, HISTORY)
    
    res = None
    try:
      res = json.loads(response.text)
    except Exception as e:
      print('No fue posible generar el json', e)
    if not res:
      continue
    HISTORY += str({"Assistant": res['Response']})
    print(res['Response'])
    if 'tool' in res and res['tool'] != None:
      res['next'] = NextType.CONTINUE.value
      tool_return = resove_tool(res['tool']['name'], res['tool']['parameters'])
      print('\033[91m', res['tool']['parameters'], '\033[0m')
      HISTORY += str({"Tool_response": tool_return})
    if res['next'] == NextType.WAIT_USER_RESPONSE.value:
      end = True
    if res['next'] == NextType.END.value:
      end = True
  return HISTORY, res