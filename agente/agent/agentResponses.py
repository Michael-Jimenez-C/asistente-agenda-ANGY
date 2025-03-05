from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(Enum):
  agregar = "agendar"
  eliminar = "eliminar"
  modificar = "modificar"
  listarPN = "listarPorNombre"
  listarPF = "listarPorFechas"
  listar = "listar"

class Evento(BaseModel):
  nombre: str
  fecha: str
  hora_inicio: str
  hora_fin: str

class Solicitud(BaseModel):
  solicitud:TipoSolicitud
  nombre: str
  fecha: str
  hora_inicio: str
  hora_fin: str

class Respuesta(BaseModel):
  status: str
  mensaje: str
  evento: Evento