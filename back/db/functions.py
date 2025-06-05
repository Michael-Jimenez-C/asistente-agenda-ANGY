from datetime import datetime
from .models import Evento
from .engine import Engine
from odmantic import query
from odmantic.bson import ObjectId

async def getEventsBeetween(fs: datetime, ff:datetime):
    r = await Engine.find(Evento, (
        query.nor_(
            query.and_(Evento.date_start >= fs, Evento.date_start >= ff),
            query.and_(Evento.date_end <= fs, Evento.date_end <= ff)
        )
    ))
    return r

async def getAllEvents():
    return await Engine.find(Evento)

async def createEvent(evento: Evento):
    evento.name = evento.name
    cruces = await getEventsBeetween(evento.date_start, evento.date_end)
    if cruces:
        return {'status': 'error', 'message': f'Ya existen eventos en ese rango de fechas {cruces}'}
    await Engine.save(evento)
    return {'status': 'ok', 'message': f'se ha agendado exitosamente {evento.name}'}

async def getEventsByName(name: str):
    eventos = await Engine.find(Evento, Evento.name == name)
    return eventos

async def putEvent(evento: Evento):
    cp_event = await Engine.find_one(Evento, Evento.id == evento.id)
    if not cp_event:
        return {'status': 'error', 'message': 'No existe el evento'}
    await Engine.delete(cp_event)
    cruces = await getEventsBeetween(evento.date_start, evento.date_end)
    if cruces:
        await Engine.save(cp_event)
        return {'status': 'error', 'message': 'Ya existe un evento en ese rango de fechas'}
    await Engine.save(evento)
    return {'status': 'ok', 'message': 'se ha actualizado exitosamente'}

async def deleteEventById(id_: ObjectId):
    cp_event = await Engine.find_one(Evento, Evento.id == id_)
    if not cp_event:
        return {'status': 'error', 'message': 'No existe el evento'}
    await Engine.delete(cp_event)
    return {'status': 'ok', 'message': 'se ha eliminado exitosamente'}