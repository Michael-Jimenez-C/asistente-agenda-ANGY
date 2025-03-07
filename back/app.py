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
        case TipoSolicitud.agregar:
            return await post_evento(solicitud)
        case TipoSolicitud.eliminar:
            return await del_evento(solicitud)
        case TipoSolicitud.eliminarEntre:
            return await del_eventos(solicitud)
        case TipoSolicitud.modificar:
            return await put_evento(solicitud)
        case TipoSolicitud.listar:
            return await get_eventos(solicitud)

@app.get("/all")
async def getAll():
    return await get_todos()
        
@app.post("/init")
async def init():
    await mocks.init()