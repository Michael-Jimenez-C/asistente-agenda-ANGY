from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(Enum):
  agregar = "agendar"
  eliminar = "eliminar"
  modificar = "modificar"
  listar = "listar"

class SolicitudBase(BaseModel):
  nombre: str
  fecha: str
  hora_inicio: str
  hora_fin: str

class Solicitud(SolicitudBase):
  solicitud:TipoSolicitud