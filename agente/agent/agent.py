from google import genai
import os
from .actions import ObtenerFecha
import json
from .agentResponses import Solicitud

API_KEY = os.environ.get("GEMINI_API_KEY")


class Roles:
  formateador = \
  """Eres un asistente que se encarga de tomar la entrada del usuario, procesarla para el formado json indicado.
  Las fechas dadas por el usuario pueden ser relativas, sin embargo, debes determinar la fecha actual y calcular la fecha en formato YYYY-MM-DD
  Las horas dadas por el usuario pueden ser relativas, sin embargo, debes determinar la hora actual y calcular la hora en formato HH:MM, en formato de 24 horas

  Por defecto si no se indica hora de fin, se toma la hora de inicio y se añade una hora
  Por defecto si no se indica hora de inicio, se toma la hora actual
  """


def context(f):
  def wrapper(input: str):
    tmp = {
        "Usuario": input,
        "Fecha actual": ObtenerFecha()
    }
    return f(str(tmp))
  return wrapper

@context
def asistente(input: str):
  client = genai.Client(api_key=API_KEY)

  response = client.models.generate_content(
      model='gemini-2.0-flash',
      config={
          'response_mime_type': 'application/json',
          'response_schema': Solicitud,
          'system_instruction':Roles.formateador
          },
      contents=[input]
  )
  res = None
  try:
    res = json.loads(response.text)
  except Exception as e:
    print('No fue posible generar el json', e)
  finally:
    return res