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
Eres ANGY, un asistente de agenda virtual. Tu función es gestionar agendas de manera eficiente, precisa y profesional.

planifica tus acciones de manera que puedas buscar la forma más eficiente de obtener la información que necesitas para resolver las peticiones de los usuarios, explicitamente explicandote a ti mismo los pasos que vas a seguir.
No improvises, siempre usas las herramientas proporcionadas para realizar calculos y recuperar información, utiliza esa retroalimentación y verifica que era lo que estabas tratando de obtener.
Utiliza esa información para poder solucionar las peticiones de los usuarios.
Tienes permitido usar herramientas para calculos auxiliares, como calcular fechas, obtener la fecha actual.
Debes respetar de las funciones los campos obligatorios y el formato de los mismos, por ejemplo las fechas YYYY-MM-DD H:M:S, como por ejemplo 2025-01-01 23:00:00.
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
      if parametro.default is inspect.Parameter.empty:
        obligatorio = "obligatoria"
      else:
        obligatorio = "opcional"
      parametros.append((nombre, tipo, obligatorio))

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

TOOLS = {i.__name__:i for i in [ObtenerFechaActual, CalcularFecha, getEventBetween, createEvent, getEventsByName, putEvent, deleteEventById]}

def resove_tool(name, params_):
  params = normalize_params(params_)
  return TOOLS[name](**params)


global CONTEXT
CONTEXT = {
    "tools": "",
    "HISTORY": "",
    "PETICION_ACTUAL": ""
}


async def asistente(input: str, proc: str = None):
  global CONTEXT
  if CONTEXT['tools']=="":
    functions = [i for i in TOOLS.values()]
    tools = {}
    for i in functions:
      desc = describer(i)
      tools[desc['nombre']] = desc["parametros"]
      print(tools)
    CONTEXT['tools']=str({"tools": tools})
  print(input)
  end = False
  CONTEXT['PETICION_ACTUAL'] = input
  brk = 0
  while not end:
    response = await model({
            'response_mime_type': 'application/json',
            'response_schema': Format,
            'system_instruction':ROLE
            }, str(CONTEXT))
    
    if CONTEXT['PETICION_ACTUAL'] != "":
      CONTEXT['HISTORY'] += "\nUser: "+CONTEXT['PETICION_ACTUAL']
      CONTEXT['PETICION_ACTUAL'] = ""
    res = None
    try:
      res = json.loads(response.text)
    except Exception as e:
      print('No fue posible generar el json', e)
    if not res:
      continue
    CONTEXT['HISTORY'] += "\nAssistant: " + res['Response']
    print(res['Response'])
    if 'tool' in res and res['tool'] != None:
      try:
        tool_return = resove_tool(res['tool']['name'], res['tool']['parameters'])
      except Exception as e:
        tool_return = str(e)
      print('\033[91m', res['tool']['name'], '\033[0m')
      print('\033[91m', res['tool']['parameters'], '\033[0m')
      print('\033[91m', tool_return, '\033[0m')
      CONTEXT['HISTORY'] += '\n'+str({"Tool_response": tool_return})
      continue
    if res['next'] == NextType.WAIT_USER_RESPONSE.value:
      end = True
    if res['next'] == NextType.END.value:
      end = True
  return CONTEXT, res