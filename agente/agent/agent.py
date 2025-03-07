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

  Si la operación podria requerir una busqueda del dia fija la hora como las 00, y hora final como las 23:59

  No puede haber más de una fecha por fecha
  """

  asistente = \
  """
  Eres un asistente que se encarga de tomar la respuesta retornada por el servidor, y la entrada del susuario para entregar una respuesta más humanizada al usuario, trata de indicar cual es el error, por ejemplo con que actividades hay cruce
  la verificación de conflictos lo realizará otro agente, asi que ignoraras esos posibles problemas, tampoco debes verificar los valores inferidos a partir de datos relativos, o si no se indica hora final pues se infiere que es dentro de una hora.
  """

def model(config, input):
  client = genai.Client(api_key=API_KEY)
  response = client.models.generate_content(
      model='gemini-2.0-flash',
      config=config,
      contents=[input]
  )
  return response

def context(f):
  def wrapper(input: str):
    tmp = {
        "Usuario": input,
        "Fecha actual": ObtenerFecha()
    }
    return f(str(tmp))
  return wrapper

@context
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

@context
def genSalida(input: str):
  response = model({
          'system_instruction':Roles.asistente
          }, input)
  return response.text


def asistente(consulta: str):
  eventos = requests.get(f"{SERVER}/all")
  response = asistente_formater(
    str({'user':consulta,
         'data': eventos.json()['data']
    })
    )
  r = requests.post(SERVER, json=response)
  try:
    json = r.json()
    ev = Evento(nombre= response['nombre'], fecha=response['fecha'], hora_inicio=response['hora_inicio'], hora_fin=response['hora_fin'])
    resp = Respuesta(status=json['status'] if 'status' in json else 'failed', mensaje=str(json['detail']), evento=ev)

    return str(genSalida(str({
      'consulta': consulta,
      'formated': response,
      'response': json,
      }))),resp.json()
  except:
    print('Error en la respuesta del servidor')
    return str(genSalida(str(r))), {"error", 'Error en la respuesta del servidor'}
