from datetime import datetime, timedelta
import pytz
import os

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