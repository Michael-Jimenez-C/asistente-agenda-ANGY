# Asistente inteligente de agenda

Este repositorio es una prueba sobre el uso de IA para hacer una interaccion humana con un sistema de agenda.

<img src="docs/chat.png"/>
<img src="docs/calendario.png"/>

# Estructura

La idea básica del funcionamiento de la aplicación es la siguiente, el usuario haria una petición que es interpretada usando un formato json dado, de forma que debe elegir el tipo de solicitud adecuado para cumplir la petición del usuario.

La entrada del usuario puede ser un audio o un chat.

Luego de ser procesada se retorna una respuesta y una LLM se encarga de procesarla junto con la respuesta de la API para entregar al usuario una respuesta en lenguaje natural.
<img src="docs/Diagrama sin título.drawio.png"></img>

# Ejecutar el proyecto
Para ejecutar es necesario un servidor de mongo, se recomienda con docker o podman para pruebas.
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements
```

copiar el ``.env.example`` como ``.env`` y colocar el token de gemini.

```sh
fastapi run back/app.py
streamlit run agente/main.py
```