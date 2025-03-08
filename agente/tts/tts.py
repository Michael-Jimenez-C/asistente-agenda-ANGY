import asyncio
import random

import edge_tts
from edge_tts import VoicesManager

VOICE = 'es-CO-GonzaloNeural'

def speech(text: str ) -> None:
    communicate = edge_tts.Communicate(text, VOICE)
    data = b""
    for chunk in communicate.stream_sync():
        if chunk['type'] == 'audio':
            data += chunk['data']
    return data