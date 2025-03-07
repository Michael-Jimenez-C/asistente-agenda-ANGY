from dotenv import load_dotenv
import pytz
import os

load_dotenv()
tz = os.environ.get("TZ")
loctz = pytz.timezone(tz)


from datetime import datetime
from agent.agent import asistente
import streamlit as st
from streamlit_calendar import calendar
from streamlit_mic_recorder import speech_to_text
from streamlit_calendar import calendar

import requests

import streamlit as st

def load():
    data = requests.get(f"{os.environ.get('SERVER')}/all").json()

    events = [{"title": x['nombre'],
            "color": "#FFBD45",
            "start": x['fecha_inicio'],
            "end": x['fecha_fin'],
            "resourceId": "a"} for x in data]
    st.session_state['events'] = events

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    response, data = asistente(user_input)
    st.session_state.generated.append(str(response))
    st.session_state.responses.append(str(data))

def send(prompt: str):
    st.session_state.past.append(prompt)
    response, data = asistente(prompt)
    st.session_state.generated.append(str(response))
    st.session_state.responses.append(str(data))


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]


col1, col2 = st.columns(2)

st.session_state.setdefault(
    'past', 
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
    'events', 
    []
)

##CHAT
col1.title("Asistente")
messages = col1.container(height=300)
if prompt := col1.chat_input("Say something"):
    send(prompt)
if text := speech_to_text("Grabar audio","Enviar",language='es',use_container_width=True,key='STT'):
    send(text)


for i in range(len(st.session_state['generated'])):
    messages.chat_message("user").write(st.session_state['past'][i])
    messages.chat_message("assistant").write(st.session_state['generated'][i])

## Responses
col2.title("Responses")
responses = col2.container(height=300)
for i in range(len(st.session_state['responses'])):
        responses.chat_message("assistant").json(st.session_state['responses'][i])

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

