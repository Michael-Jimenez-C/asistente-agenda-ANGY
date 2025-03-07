from db.models import Evento
from db.engine import Engine
from datetime import datetime

async def init():
    await Engine.save_all([
        Evento(nombre="Llamada con cliente", fecha_inicio=datetime(2025,3,10,13,30), fecha_fin=datetime(2025,3,10,14,30)),
        Evento(nombre="Revisión de código", fecha_inicio=datetime(2025,3,10,15,0), fecha_fin=datetime(2025,3,10,16,0)),
    ])