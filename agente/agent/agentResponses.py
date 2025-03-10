from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(str,Enum):
  AGREGAR = "agendar"
  ELIMINAR_UNO = "eliminarUno"
  ELIMINAR_VARIOS = "eliminarEntre"
  MODIFICAR = "modificar"
  LISTAR = "listar"
  NADA = "NADA"

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