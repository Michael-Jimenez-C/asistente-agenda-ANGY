from fastapi import FastAPI
from interfaces import Solicitud, TipoSolicitud
from dotenv import load_dotenv
import mocks

load_dotenv()

from db.functions import get_eventos, post_evento, put_evento, del_evento, get_todos, del_eventos

app = FastAPI()

@app.post("/")
async def procesarSolicitud(solicitud: Solicitud):
    
    match solicitud.solicitud:
        case TipoSolicitud.AGREGAR:
            return await post_evento(solicitud)
        case TipoSolicitud.ELIMINAR_UNO:
            return await del_evento(solicitud)
        case TipoSolicitud.ELIMINAR_VARIOS:
            return await del_eventos(solicitud)
        case TipoSolicitud.MODIFICAR:
            return await put_evento(solicitud)
        case TipoSolicitud.LISTAR:
            return await get_eventos(solicitud)

@app.get("/all")
async def getAll():
    return await get_todos()
        
@app.post("/init")
async def init():
    await mocks.init()