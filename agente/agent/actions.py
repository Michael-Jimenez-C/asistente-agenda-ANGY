from datetime import datetime
import pytz
import os
tz = os.environ.get("TZ")
loctz = pytz.timezone(tz)

def ObtenerFecha():
  return str(datetime.now(loctz).strftime('%Y-%m-%d %H:%M | Hoy es %A %d de %B'))