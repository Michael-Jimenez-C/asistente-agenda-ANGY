from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from db.functions import getEventsBeetween, createEvent, getEventsByName, putEvent, deleteEventById, getAllEvents
from datetime import datetime
from db.models import Evento
from odmantic.bson import ObjectId

app = FastAPI()

@app.get("/between")
async def Beetween(date_start: datetime, date_end: datetime):
    return await getEventsBeetween(date_start, date_end)

@app.post("/create")
async def createEvent_(evento: Evento):
    return await createEvent(evento)

@app.get("/event/{name}")
async def getEventsByName_(name: str):
    return await getEventsByName(name)

@app.put("/")
async def putEvent_(evento: Evento):
    return await putEvent(evento)

@app.delete("/delete/{id_}")
async def deleteEventById_(id_: ObjectId):
    return await deleteEventById(id_)

@app.get("/all")
async def getAll():
    return await getAllEvents()