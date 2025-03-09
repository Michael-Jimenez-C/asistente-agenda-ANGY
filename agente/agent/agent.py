from google import genai
import os
from .actions import ObtenerFecha
import json
from .agentResponses import Solicitud, Evento, Respuesta
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")
SERVER = os.environ.get("SERVER")

class Roles:
  formateador = \
  """Eres un asistente que se encarga de tomar la entrada del usuario, procesarla para el formado json indicado.

  Las fechas dadas por el usuario pueden ser relativas, sin embargo, debes determinar la fecha actual y calcular la fecha en formato YYYY-MM-DD
  Las horas dadas por el usuario pueden ser relativas, sin embargo, debes determinar la hora actual y calcular la hora en formato HH:MM, en formato de 24 horas

  Por defecto si no se indica hora de fin, se toma la hora de inicio y se añade una hora
  Por defecto si no se indica hora de inicio, se toma la hora actual

  Si la operación es borrar varios un dia, toma la hora como 00:00, y hora final como las 23:59

  No puede haber más de una fecha por fecha

  Para borrar debes conocer nombre, fecha, hora de inicio y hora final
  """

  asistente = \
  """
  Eres un asistente que se encarga de tomar la respuesta retornada por el servidor, y la entrada del susuario para entregar una respuesta más humanizada al usuario, trata de indicar cual es el error, por ejemplo con que actividades hay cruce
  la verificación de conflictos lo realizará otro agente, asi que ignoraras esos posibles problemas, tampoco debes verificar los valores inferidos a partir de datos relativos, o si no se indica hora final pues se infiere que es dentro de una hora.
  adicional recuerda que el usuario podria expresarse con tiempos relativos, mañana, ayer, en una hora, etc.
  """

def model(config, input):
  client = genai.Client(api_key=API_KEY)
  response = client.models.generate_content(
      model='gemini-2.0-flash',
      config=config,
      contents=[input]
  )
  return response

def context(**kwargs):
  """
  Ese decorador de contexto se encarga de recibir un conjunto de funciones a ejecutar y las asigna a un diccionario
  junto a la entrada
  """
  def context_(f):
    def wrapper(input: str):
      tmp = {
          "Usuario": input
      }
      for i in kwargs:
        tmp[i] = kwargs[i]()
      return f(str(tmp))
    return wrapper
  return context_

@context(fecha_actual = ObtenerFecha, eventos = lambda: requests.get(f"{SERVER}/all").json())
def asistente_formater(input: str):
  response = model({
          'response_mime_type': 'application/json',
          'response_schema': Solicitud,
          'system_instruction':Roles.formateador
          }, input)
  res = None
  try:
    res = json.loads(response.text)
  except Exception as e:
    print('No fue posible generar el json', e)
  finally:
    return res

@context(fecha_actual = ObtenerFecha)
def genSalida(input: str):
  response = model({
          'system_instruction':Roles.asistente
          }, input)
  return response.text


def asistente(consulta: str):
  response = asistente_formater(consulta)
  r = requests.post(SERVER, json=response)
  json = r.json()
  context.append(json)

  ev = Evento(nombre= response['nombre'], fecha=response['fecha'], hora_inicio=response['hora_inicio'], hora_fin=response['hora_fin'])
  resp = Respuesta(status=json['status'] if 'status' in json else 'failed', mensaje=str(json['detail']), evento=ev)

  return str(genSalida(str({
    'consulta': consulta,
    'formated': response,
    'response': json,
    }))),resp.json()
