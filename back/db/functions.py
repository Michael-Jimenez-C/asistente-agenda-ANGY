from .models import Evento
from .engine import Engine
from interfaces import SolicitudBase
from odmantic import query

async def get_eventos(solicitud):
    r = await Engine.find(Evento, (
        query.nor_(
            query.and_(Evento.fecha_inicio >= solicitud.fecha_inicio, Evento.fecha_inicio >= solicitud.fecha_fin),
            query.and_(Evento.fecha_fin <= solicitud.fecha_inicio, Evento.fecha_fin <= solicitud.fecha_fin)
        )
    ))
    return {'status':'ok',
            'detail': '',
            'data':[SolicitudBase(nombre=e.nombre, fecha=e.fecha_inicio.strftime('%Y-%m-%d'), hora_inicio=e.fecha_inicio.strftime('%H:%M'), hora_fin=e.fecha_fin.strftime('%H:%M')) for e in r]}



async def post_evento(solicitud):
    if solicitud.fecha_inicio >= solicitud.fecha_fin:
        return {
                'status':'failed',
                'detail':'la fecha de inicio no puede ser mayor ni igual a la fecha de fin'
                }
    
    cruce = await get_eventos(solicitud)
    if cruce['data']:
        return {
                'status':'failed',
                'detail':f'Se presenta cruce con {" ".join([f"{e.nombre}, {e.hora_inicio}, {e.hora_fin}" for e in cruce['data']])}'
                }
    
    evento = Evento(nombre=solicitud.nombre, fecha_inicio=solicitud.fecha_inicio, fecha_fin=solicitud.fecha_fin)
    await Engine.save(evento)
    return {
            'status':'Ok',
            'detail':'Se guardó correctamente'
            }



async def put_evento(solicitud):    
    evento = await Engine.find_one(Evento, Evento.nombre == solicitud.nombre)
    if not evento:
        return {
                'status':'failed',
                'detail':'No se encontró el evento'
                }

    cruce = await get_eventos(solicitud)
    if len(cruce['data']) > 1 and cruce['data'][0].nombre != solicitud.nombre:
        return {
                'status':'failed',
                'detail':f'Se presenta cruce con {" ".join([f"{e.nombre}, {e.hora_inicio}, {e.hora_fin}" for e in cruce['data']])}'
                }
    
    evento.fecha_inicio = solicitud.fecha_inicio
    evento.fecha_fin = solicitud.fecha_fin
    await Engine.save(evento)
    return {
            'status':'Ok',
            'detail':'Se guardó correctamente el cambio'
            }

async def del_evento(solicitud):
    ev_dv = await Engine.find_one(Evento, Evento.nombre == solicitud.nombre, Evento.fecha_inicio == solicitud.fecha_inicio, Evento.fecha_fin == solicitud.fecha_fin)
    if not ev_dv:
        return {
                'status':'failed',
                'detail':'No se encontró el evento'
                }
    await Engine.delete(ev_dv)
    return {
            'status':'Ok',
            'detail':'Se eliminó correctamente'
            }

async def del_eventos(solicitud):
    await Engine.remove(Evento, Evento.fecha_inicio >= solicitud.fecha_inicio, Evento.fecha_fin <= solicitud.fecha_fin)
    return {
            'status':'Ok',
            'detail':'Se eliminó correctamente'
            }

async def get_todos():
    r = await Engine.find(Evento)
    return {'status':'ok',
            'detail': '',
            'data':r
            }