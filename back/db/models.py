from odmantic import Model
from datetime import datetime

class Evento(Model):
    name: str
    description: str
    location: str
    date_start: datetime
    date_end : datetime