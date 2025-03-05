from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
import os

uri = os.environ.get('MONGO_URI')
client = AsyncIOMotorClient(uri)

Engine = AIOEngine(client, database='agenda')