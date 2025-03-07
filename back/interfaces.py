from pydantic import BaseModel, model_validator

from enum import Enum
from datetime import date, time, datetime

class TipoSolicitud(str,Enum):
  AGREGAR = "agendar"
  ELIMINAR_UNO = "eliminarUno"
  ELIMINAR_VARIOS = "eliminarEntre"
  MODIFICAR = "modificar"
  LISTAR = "listar"

class SolicitudBase(BaseModel):
  nombre: str
  fecha: date
  hora_inicio: time
  hora_fin: time

  class Config:
      json_encoders = {
          date: lambda v: v.strftime("%y-%-m-%-d"),
          time: lambda v: v.strftime("%-H:%-M"),
      }

  @property
  def fecha_inicio(self) -> datetime:
      """Combina fecha y hora_inicio en un solo datetime."""
      return datetime.combine(self.fecha, self.hora_inicio)

  @property
  def fecha_fin(self) -> datetime:
      """Combina fecha y hora_fin en un solo datetime."""
      return datetime.combine(self.fecha, self.hora_fin)
  
  @model_validator(mode="after")
  def validar_fechas(self):
      """Valida que la fecha y hora de inicio no sean después de la fecha y hora de fin."""
      if self.fecha_inicio > self.fecha_fin:
          raise ValueError("La fecha y hora de inicio deben ser anteriores a la fecha y hora de fin.")
      return self

class Solicitud(SolicitudBase):
  solicitud:TipoSolicitud

class Evento(BaseModel):
    nombre: str
    fecha_inicio: datetime
    fecha_fin: datetime