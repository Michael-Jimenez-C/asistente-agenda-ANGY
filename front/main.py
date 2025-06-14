from dotenv import load_dotenv
import pytz
import os
import uuid

load_dotenv()
tz = os.environ.get("TZ")
loctz = pytz.timezone(tz)


from datetime import datetime
import streamlit as st
from streamlit_calendar import calendar
from streamlit_mic_recorder import speech_to_text
from streamlit_calendar import calendar

import requests

import streamlit as st


from tts.tts import speech




def load():
    data = requests.get(f"{os.environ.get('SERVER')}/all").json()

    events = [{"title": x['name'],
            "color": "#FFBD45",
            "start": x['date_start'],
            "end": x['date_end'],
            "resourceId": "a"} for x in data]
    st.session_state['events'] = events

def send(prompt: str):
    response = requests.post(f"{os.environ.get('SERVER_AGENTE')}/",json = {"solicitud": prompt, "proc": "user"})
    for resp in response.json():
        st.session_state.past.append(prompt)
        prompt = None

        generated = resp.get('Asistant', {})

        st.session_state.generated.append(generated.get('Response', None))
        st.session_state.toolcall.append(generated.get('tool', None))
        st.session_state.responses.append(generated)

        st.session_state.audio.append(None)
    st.session_state.audio[-1] = speech(str(st.session_state.generated[-1]))

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


col1, col2 = st.columns(2)

st.session_state.setdefault(
    'past', 
    []
)
st.session_state.setdefault(
    'toolcall', 
    []
)
st.session_state.setdefault(
    'generated', 
    []
)

st.session_state.setdefault(
    'responses', 
    []
)


st.session_state.setdefault(
    'audio', 
    []
)

st.session_state.setdefault(
    'events', 
    []
)

##CHAT
col1.title("Asistente")
messages = col1.container(height=400)
if prompt := col1.chat_input("Say something"):
    send(prompt)
with col1:
    if text := speech_to_text("Grabar audio","Enviar",language='es',use_container_width=True,key='STT'):
        send(text)


for i in range(len(st.session_state['generated'])):
    if st.session_state['past'][i]:
        messages.chat_message("user").write(st.session_state['past'][i])

    if st.session_state['generated'][i]:
        messages.chat_message("assistant").write(st.session_state['generated'][i])
    if st.session_state['toolcall'][i]:
        messages.chat_message("assistant").json(st.session_state['toolcall'][i], expanded=1)

    if st.session_state['audio'][i]:
        messages.chat_message("assistant").audio(st.session_state['audio'][i],autoplay=True)

## Responses
col2.title("Responses")
responses = col2.container(height=400)
for i in range(len(st.session_state['responses'])):
        if st.session_state['responses'][i] and st.session_state['responses'][i] != {}:
            responses.chat_message("assistant").json(st.session_state['responses'][i], expanded=1)


calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]

calendar_options = {
            "editable": True,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
            },
            "slotMinTime": "03:00:00",
            "slotMaxTime": "12:00:00",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": str(datetime.now(loctz).strftime('%Y-%m-%d')),
            "initialView": "dayGridMonth",
            "resources": calendar_resources,
        }


st.title("Agenda actual")

load()
if st.session_state.get('events'):
    calendar = calendar(
        events=st.session_state['events'],
        options=calendar_options,
        key='calendar'
        )