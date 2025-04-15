from fastapi import FastAPI
from dotenv import load_dotenv
from interfaces import Solicitud
load_dotenv()
from agent.agent import asistente

app = FastAPI()

@app.post("/")
async def procesar_solicitud(solicitud:Solicitud):
    return await asistente(solicitud.solicitud, solicitud.proc)