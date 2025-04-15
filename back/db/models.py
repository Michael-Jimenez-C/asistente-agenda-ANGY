from odmantic import Model
from datetime import datetime

class Evento(Model):
    nombre: str
    descripcion: str
    lugar: str
    fecha_inicio: datetime
    fecha_fin : datetime