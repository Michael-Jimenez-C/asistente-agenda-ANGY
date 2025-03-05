from fastapi import FastAPI
from formats import Solicitud, TipoSolicitud
from dotenv import load_dotenv
load_dotenv()

from db.functions import get_eventos, post_evento

app = FastAPI()

@app.post("/")
async def procesarSolicitud(solicitud: Solicitud):
    
    match solicitud.solicitud:
        case TipoSolicitud.agregar:
            return await post_evento(solicitud)
        case TipoSolicitud.eliminar:
            pass
        case TipoSolicitud.modificar:
            pass
        case TipoSolicitud.listar:
            return await get_eventos(solicitud)