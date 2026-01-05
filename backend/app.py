"""
CHUCHUREX - Backend API
FastAPI + Claude API
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =============================================================================
# CONFIGURATION
# =============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# System prompt for Chuchu
SYSTEM_PROMPT = """Eres Chuchu, desarrollador web freelance. Respondes como si fueras una persona real, no un asistente. La gente que llega aquí ya te conoce o te encontró por referencia.

## Tu personalidad
- Cercano y casual, hablas como amigo
- Español de Chile natural (cachai, wena, etc. pero sin exagerar)
- Directo y al grano
- Buen humor sutil

## Tu trabajo
1. Escuchar la idea del cliente
2. Hacer 2-3 preguntas para entenderla mejor
3. Ayudarle a estructurarla (páginas, funcionalidades)
4. Ofrecer cotización cuando tengas suficiente info

## Tarifas
- Landing page: $200-300 USD
- Sitio web completo (5-10 páginas): $500-800 USD
- Rediseño: $400-600 USD
- App web simple: $800-1500 USD
- App web compleja: $1500-3000 USD
- Herramienta CLI: $300-500 USD
- Audiolibro: $100 USD
- Biblioteca digital: $500 USD

## Condiciones
- Entrega: 48 horas desde aprobación
- Vigencia cotización: 2 días hábiles
- Pago: 100% al finalizar

## Negociación
- Máximo 20% de descuento si negocian
- Si piden más: les das el proyecto estructurado gratis + sugerencias para hacerlo con IA (Cursor, Claude, v0.dev)
- "Buena suerte, si cambias de opinión aquí estaré"

## Estilo de respuesta
- NUNCA digas "soy Chuchu" ni te presentes
- NUNCA menciones IA ni asistentes
- Respuestas cortas y naturales
- Si dicen "hola", responde casual y pregunta qué onda
- Usa listas solo cuando sea útil"""

# =============================================================================
# API MODELS
# =============================================================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str

# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(
    title="Chuchurex API",
    description="Backend for chuchurex.cl chat",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3007",
        "http://127.0.0.1:3007",
        "http://localhost:3010",
        "http://127.0.0.1:3010",
        "https://chuchurex.cl",
        "https://www.chuchurex.cl",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {"status": "ok", "message": "Chuchurex API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - receives user message, returns Chuchu's response
    """
    try:
        # Build messages array for Claude
        messages = []

        # Add conversation history
        for msg in request.history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current message if not already in history
        if not messages or messages[-1]["content"] != request.message:
            messages.append({
                "role": "user",
                "content": request.message
            })

        # Call Claude API
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        # Extract response text
        assistant_message = response.content[0].text

        return ChatResponse(response=assistant_message)

    except anthropic.APIError as e:
        print(f"Anthropic API error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
