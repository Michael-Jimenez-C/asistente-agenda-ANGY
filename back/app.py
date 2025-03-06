from fastapi import FastAPI
from formats import Solicitud, TipoSolicitud
from dotenv import load_dotenv
import tests

load_dotenv()

from db.functions import get_eventos, post_evento, mod_evento, del_evento, get_eventos_total

app = FastAPI()

@app.post("/")
async def procesarSolicitud(solicitud: Solicitud):
    
    match solicitud.solicitud:
        case TipoSolicitud.agregar:
            return await post_evento(solicitud)
        case TipoSolicitud.eliminar:
            return await mod_evento(solicitud)
        case TipoSolicitud.modificar:
            return await del_evento(solicitud)
        case TipoSolicitud.listar:
            return await get_eventos(solicitud)

@app.get("/all")
async def getAll():
    return await get_eventos_total()
        
@app.post("/init")
async def init():
    await tests.init()