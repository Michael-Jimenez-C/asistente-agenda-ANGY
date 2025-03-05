from .models import Evento
from .engine import Engine
from datetime import datetime
from formats import SolicitudBase

from odmantic import query


def procesarFechas(solicitud):
    fecha_inicio = datetime.strptime(solicitud.fecha+' '+solicitud.hora_inicio, '%Y-%m-%d %H:%M')
    fecha_fin = datetime.strptime(solicitud.fecha+' '+solicitud.hora_fin, '%Y-%m-%d %H:%M')
    return fecha_inicio, fecha_fin

async def get_eventos(solicitud):
    fecha_inicio, fecha_fin = procesarFechas(solicitud)
    r = await Engine.find(Evento, (
        query.nor_(
            query.and_(Evento.fecha_inicio >= fecha_inicio, Evento.fecha_inicio >= fecha_fin),
            query.and_(Evento.fecha_fin <= fecha_inicio, Evento.fecha_fin <= fecha_fin)
        )
    ))
    return [SolicitudBase(nombre=e.nombre, fecha=e.fecha_inicio.strftime('%Y-%m-%d'), hora_inicio=e.fecha_inicio.strftime('%H:%M'), hora_fin=e.fecha_fin.strftime('%H:%M')) for e in r]



async def post_evento(solicitud):
    procesarFechas(solicitud)
    fecha_inicio, fecha_fin = procesarFechas(solicitud)
    if fecha_inicio >= fecha_fin:
        return {
                'status':'failed',
                'detail':'la fecha de inicio no puede ser mayor ni igual a la fecha de fin'
                }
    
    cruce = await get_eventos(solicitud)
    if cruce:
        return {
                'status':'failed',
                'detail':f'Se presenta cruce con {" ".join([f"{e.nombre}, {e.hora_inicio}, {e.hora_fin}" for e in cruce])}'
                }
    
    evento = Evento(nombre=solicitud.nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    await Engine.save(evento)
    return {
            'status':'Ok',
            'detail':'Se guardó correctamente'
            }