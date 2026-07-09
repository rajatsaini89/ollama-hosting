import os
import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ollama API")

OLLAM_BASE_URL = os.getenv("OLLAM_BASE_URL", "http://localhost:11434")  # Default to localhost if not set
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2")  # Default model if not set

class PromptRequest(BaseModel):
    prompt: str
    model: str = DEFAULT_MODEL  # Use the default model if not provider

@app.get("/")
def home():
    return {
        "message": "Ollama API is running",
        "endpoints": {
            "health": "/health",
            "models": "/models",
            "generate": "/generate",
        }
    }

@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient() as Client:
            response = await Client.get(f"{OLLAM_BASE_URL}/api/tags")

        return {
            "status": "healthy",
            "models": response.json()["models"]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
    
@app.get("/models")
async def models():
    try:
        async with httpx.AsyncClient() as Client:
            response = await Client.get(f"{OLLAM_BASE_URL}/api/tags")

        return {
            "models": response.json()["models"]
        }
    except Exception as e:
        return {
            "error": str(e)
        }

@app.post("/generate")
async def generate(prompt_request: PromptRequest):
    payload = {
                    "model": prompt_request.model,
                    "prompt": prompt_request.prompt,
                    "stream": False
                }
    try:
        async with httpx.AsyncClient(timeout=120) as Client:
            response = await Client.post(
                f"{OLLAM_BASE_URL}/api/generate",
                json=payload
            )

        return {
            "response": response.json()
        }
    except Exception as e:
        return {
            "error": str(e)
        }