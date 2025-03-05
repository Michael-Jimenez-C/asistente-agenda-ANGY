from odmantic import Model
from datetime import datetime

class Evento(Model):
    nombre: str
    fecha_inicio: datetime
    fecha_fin : datetime
    