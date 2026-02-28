from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests

app = FastAPI()

# servir carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# abrir la web
@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

class Pregunta(BaseModel):
    texto: str

@app.post("/preguntar")
def preguntar(p: Pregunta):
    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "phi3",
                "prompt": p.texto,
                "stream": False
            },
            timeout=120
        )

        if r.status_code != 200:
            return JSONResponse({
                "respuesta": "Error interno en Ollama."
            })

        data = r.json()
        return JSONResponse({
            "respuesta": data.get("response", "No tengo respuesta ahora mismo.")
        })

    except requests.exceptions.ConnectionError:
        return JSONResponse({
            "ollama_required": True
        })

    except Exception as e:
        return JSONResponse({
            "respuesta": f"Error: {str(e)}"
        })