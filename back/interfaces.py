from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(str,Enum):
  agregar = "agendar"
  eliminar = "eliminar"
  eliminarEntre = "eliminarEntre"
  modificar = "modificar"
  listar = "listar"

class SolicitudBase(BaseModel):
  nombre: str
  fecha: str
  hora_inicio: str
  hora_fin: str

class Solicitud(SolicitudBase):
  solicitud:TipoSolicitud