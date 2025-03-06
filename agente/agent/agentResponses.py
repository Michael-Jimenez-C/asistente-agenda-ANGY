from pydantic import BaseModel
from enum import Enum

class TipoSolicitud(str,Enum):
  agregar = "agendar"
  eliminar = "eliminar"
  modificar = "modificar"
  listar = "listar"

class Conocimiento(str,Enum):
  AmbiguedadEnNombre = "ambiguedad en nombre"
  AmbiguedadEnFechas = "ambiguedad en fechas"
  InformacionSuficiente = "Informacion suficiente"
  BuscarPorFecha = "buscar por fecha"


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