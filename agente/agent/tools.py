from datetime import datetime, timedelta
import pytz
import os
import requests
SERVER = os.environ.get("SERVER")

tz = os.environ.get("TZ", "America/Bogota")
loctz = pytz.timezone(tz)

def ObtenerFechaActual() -> str:
  """
  Recupera la fecha actual
  """
  return str(datetime.now(loctz).strftime('%Y-%m-%d %H:%M:%S | Hoy es %A %d de %B'))

def CalcularFecha(date:datetime, days:int = 0, weeks:int = 0, hours:int = 0, minutes:int = 0) -> str:
  try:
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    days = int(days)
    weeks = int(weeks)
    hours = int(hours)
    minutes = int(minutes)
    return str((date + timedelta(days=days, weeks=weeks, hours=hours, minutes=minutes)).strftime('%Y-%m-%d %H:%M | fecha %A %d de %B'))
  except Exception as e:
    return str(e) + " | Error al calcular la fecha, revisa el formato de la fecha de entrada"

def getEventBetween(date_start: datetime, date_end: datetime):
    try:
        url = f"{SERVER}/between"  
        params = {
            "date_start": date_start,
            "date_end": date_end
        }
        response = requests.get(url, params=params) 
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Error no se pudo obtener respuesta del servidor: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Excepción al realizar la solicitud: {str(e)}"}
  
def createEvent(name: str, date_start: datetime, date_end: datetime, description: str = None, location: str = None):
    try:
        url = f"{SERVER}/create"
        data = {
            "name": name,
            "description": description,
            "location": location,
            "date_start": date_start,
            "date_end": date_end
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return {"status": "success", "message": "Evento creado exitosamente"}
        else:
            return {"status": "error", "message": f"Error no se pudo obtener respuesta del servidor: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Excepción al realizar la solicitud: {str(e)}"}
  
def getEventsByName(name: str):
    try:
        url = f"{SERVER}/event/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Error no se pudo obtener respuesta del servidor: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Excepción al realizar la solicitud: {str(e)}"}

def putEvent(id_: str, name: str, date_start: datetime, date_end: datetime, description: str = None, location: str = None):
    try:
        url = f"{SERVER}/"
        data = {
            "id": id_,
            "name": name,
            "description": description,
            "location": location,
            "date_start": date_start,
            "date_end": date_end
        }
        response = requests.put(url, json=data)
        if response.status_code == 200:
            return {"status": "success", "message": "Evento actualizado exitosamente"}
        else:
            return {"status": "error", "message": f"Error no se pudo obtener respuesta del servidor: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Excepción al realizar la solicitud: {str(e)}"}
    

def deleteEventById(id_: str):
    try:
        url = f"{SERVER}/delete/{id_}"
        response = requests.delete(url)
        if response.status_code == 200:
            return {"status": "success", "message": "Evento eliminado exitosamente"}
        else:
            return {"status": "error", "message": f"Error no se pudo obtener respuesta del servidor: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"Excepción al realizar la solicitud: {str(e)}"}