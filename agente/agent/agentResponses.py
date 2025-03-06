from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(str,Enum):
  agregar = "agendar"
  eliminarUno = "eliminar"
  eliminarVarios = "eliminarEntre"
  modificar = "modificar"
  listar = "listar"

class Evento(BaseModel):
  nombre: str
  fecha: str
  hora_inicio: str
  hora_fin: str

class Solicitud(Evento):
  solicitud:TipoSolicitud

class Respuesta(BaseModel):
  status: str
  mensaje: str
  evento: Evento