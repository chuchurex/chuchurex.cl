"""
CHUCHUREX - Backend API
FastAPI + Claude API
"""

import os
import json
import random
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Directorios
CHATS_DIR = "/var/www/chuchurex-api/chats"
PDF_GENERATOR_DIR = "/var/www/chuchurex-api/pdf-generator"
PROPOSALS_DIR = "/var/www/chuchurex-api/proposals"
os.makedirs(CHATS_DIR, exist_ok=True)
os.makedirs(PROPOSALS_DIR, exist_ok=True)

# Saludos aleatorios
SALUDOS_CON_PREGUNTA = [
    "Hola, ¿cómo te puedo ayudar? ¿Tienes alguna idea o proyecto en mente?",
    "¡Hola! Cuéntame, ¿qué tienes en mente?",
    "Hola, ¿en qué te puedo echar una mano?",
    "¡Hola! ¿Qué proyecto te trae por acá?",
    "Hola, cuéntame tu idea.",
    "¡Hola! ¿Qué andas buscando?",
    "Hola, ¿con qué te puedo ayudar hoy?",
    "¡Hola! ¿Qué necesitas?",
    "Hola, estoy para ayudarte. ¿Qué tienes en mente?",
    "¡Hola! Cuéntame en qué andas.",
    "Hola, ¿qué proyecto tienes entre manos?",
    "¡Hola! ¿En qué puedo apoyarte?",
]

SALUDOS_SIMPLES = [
    "Hola, perfecto.",
    "¡Hola! Dale, cuéntame.",
    "Hola, te escucho.",
    "¡Hola! Súper.",
    "Hola.",
    "¡Hola! Excelente.",
    "Hola, entiendo.",
    "¡Hola! Genial.",
    "Hola, claro.",
]

def get_saludo(user_already_explained=False):
    if user_already_explained:
        return random.choice(SALUDOS_SIMPLES)
    return random.choice(SALUDOS_CON_PREGUNTA)

def save_chat(messages: list, response: str):
    """Guarda la conversación para análisis durante beta"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CHATS_DIR}/chat_{timestamp}.json"
        data = {
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "response": response
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        pass

SYSTEM_PROMPT = """Eres el asistente virtual de Chuchurex, un desarrollador web freelance chileno.

Tu rol es AYUDAR a las personas con sus proyectos web. El modelo de negocio no es vender a toda costa, sino ser útil.

Personalidad:
- Amigable y cercano, pero profesional
- Lenguaje coloquial sin modismos marcados (usa "dale", "súper", evita "bacán", "cachai", etc.)
- Respuestas claras y concisas
- Lenguaje inclusivo neutral

REGLA CRÍTICA DE FORMATO:
- Responde con UN SOLO párrafo corto
- Termina con UNA SOLA pregunta (si corresponde)
- NUNCA hagas múltiples preguntas
- Máximo 2-3 oraciones + 1 pregunta final

PARA SALUDOS INICIALES ("hola", "buenas", etc.):
Usa este saludo exacto: "{saludo}"

FILOSOFÍA DE SERVICIO:
- Ayudar primero, vender después
- Si alguien no quiere presupuesto, igual ayúdale con un pre-proyecto o estructura
- Si muestran interés en cotizar, ofrece la cotización
- Si solo quieren orientación, dásela gratis
- Siempre dejar algo útil al visitante

SERVICIOS:
- Desarrollo web (landing pages, sitios, apps)
- WordPress y cualquier CMS
- Código custom
- Soporte técnico (instalar códigos, píxeles, etc.)

TARIFAS (solo si las piden o muestran interés en contratar):
- Landing page: -300 USD
- Sitio web completo: -800 USD
- Rediseño: -600 USD
- App web simple: -1500 USD
- App web compleja: -3000 USD
- Soporte técnico puntual: -50 USD

SI NO QUIEREN CONTRATAR:
Ofrece entregarles un pre-proyecto gratis con:
- Estructura sugerida del sitio
- Funcionalidades recomendadas
- Tecnologías sugeridas
- Pueden hacerlo ellos o volver cuando quieran

PROPUESTA EN PDF - DETECCIÓN INTELIGENTE:

CUÁNDO OFRECER la propuesta en PDF (cualquiera de estas condiciones):
A) VOLUMEN: Han intercambiado 6+ mensajes Y el usuario ha explicado su idea con detalle
B) PALABRAS CLAVE: El usuario menciona "presupuesto", "cuánto cuesta", "cotización", "precio", "contratar"
C) PRÓXIMOS PASOS: El usuario pregunta "qué sigue", "cómo seguimos", "próximos pasos"

Cuando detectes estas condiciones, OFRECE la propuesta:
"¿Te gustaría que te prepare un documento con todo lo que hemos conversado? Te puedo generar un PDF."

CUÁNDO ACTIVAR el PDF (DEBES incluir [PDF_TRIGGER]):
- Si el usuario ACEPTA tu oferta (dice "sí", "dale", "perfecto", "quiero", etc.)
- Si el usuario PIDE directamente una propuesta/cotización/documento desde el inicio

CRÍTICO - Cuando aceptes generar el PDF, tu respuesta DEBE terminar con [PDF_TRIGGER]:

✅ RESPUESTAS CORRECTAS (todas terminan con el trigger):
- "Perfecto, te preparo el documento ahora. [PDF_TRIGGER]"
- "Dale, te armo la propuesta. [PDF_TRIGGER]"
- "Excelente, generando tu propuesta. [PDF_TRIGGER]"
- "Claro, te genero el PDF ahora. [PDF_TRIGGER]"

❌ RESPUESTA INCORRECTA (falta el trigger):
- "Perfecto, te preparo el documento ahora." (sin [PDF_TRIGGER])
- Cualquier respuesta que prometa PDF pero NO incluya [PDF_TRIGGER]

REGLA: Si dices que vas a preparar/generar/crear un PDF, SIEMPRE agrega [PDF_TRIGGER] al final.

CIERRE:
- Si muestran interés en contratar: "¿Te gustaría que coordinemos? Escríbeme a carlos@chuchurex.cl"
- Si solo querían info: "Espero haberte ayudado. Si necesitas algo más, aquí estaré."

IMPORTANTE:
- NUNCA digas que eres "Chuchu" ni te pongas nombre
- NUNCA menciones que eres IA
- NUNCA digas que no puedes hacer algo
- Responde como parte del equipo de Chuchurex"""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    generate_pdf: Optional[bool] = False
    pdf_url: Optional[str] = None

app = FastAPI(title="Chuchurex API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chuchurex.cl", "https://www.chuchurex.cl"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "message": "Chuchurex API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/chats", response_class=HTMLResponse)
async def view_chats(key: str = Query(None)):
    if key != "chuchu2026":
        return HTMLResponse("<h1>Acceso denegado</h1>", status_code=403)
    
    chats = []
    try:
        for filename in sorted(os.listdir(CHATS_DIR), reverse=True):
            if filename.endswith(".json"):
                filepath = os.path.join(CHATS_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    chat_data = json.load(f)
                    chats.append(chat_data)
    except Exception as e:
        pass
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chats Beta - Chuchurex</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #F5F0E6; padding: 2rem; }
            h1 { color: #722F37; margin-bottom: 2rem; }
            .chat { background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .timestamp { color: #888; font-size: 0.85rem; margin-bottom: 1rem; }
            .message { padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 0.5rem; }
            .user { background: #722F37; color: white; margin-left: 20%; }
            .assistant { background: #eee; margin-right: 20%; }
            .empty { text-align: center; color: #888; padding: 3rem; }
            .count { color: #888; margin-bottom: 1rem; }
        </style>
    </head>
    <body>
        <h1>Chats Beta - Chuchurex</h1>
        <p class="count">Total: """ + str(len(chats)) + """ conversaciones</p>
    """
    
    if not chats:
        html += '<div class="empty">No hay chats guardados todavía.</div>'
    else:
        for chat in chats:
            html += f'<div class="chat"><div class="timestamp">{chat.get("timestamp", "Sin fecha")}</div>'
            for msg in chat.get("messages", []):
                role_class = "user" if msg["role"] == "user" else "assistant"
                html += f'<div class="message {role_class}">{msg["content"]}</div>'
            html += f'<div class="message assistant">{chat.get("response", "")}</div>'
            html += '</div>'
    
    html += "</body></html>"
    return HTMLResponse(html)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = []
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})
        if not messages or messages[-1]["content"] != request.message:
            messages.append({"role": "user", "content": request.message})

        # Detectar si el primer mensaje del usuario ya explica su proyecto
        user_already_explained = False
        if len(messages) == 1:  # Solo primer mensaje
            first_msg = messages[0]["content"].lower()
            # Si el mensaje tiene más de 10 palabras Y menciona algo específico
            palabra_count = len(first_msg.split())
            keywords = ["quiero", "necesito", "modernizar", "rediseñ", "crear", "hacer", "mejorar", "website", "sitio", "web", "página", "app"]
            tiene_keyword = any(kw in first_msg for kw in keywords)

            if palabra_count > 10 and tiene_keyword:
                user_already_explained = True

        # Insertar saludo aleatorio en el prompt
        current_prompt = SYSTEM_PROMPT.replace("{saludo}", get_saludo(user_already_explained))

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=current_prompt,
            messages=messages
        )
        response_text = response.content[0].text

        save_chat(messages, response_text)

        # Detectar si debe generar PDF
        if "[PDF_TRIGGER]" in response_text:
            try:
                # Generar PDF automáticamente
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_base = f"propuesta_cliente_{timestamp}"
                md_path = f"{PROPOSALS_DIR}/{filename_base}.md"
                pdf_path = f"{PROPOSALS_DIR}/{filename_base}.pdf"

                # Analizar conversación con Claude Sonnet
                conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

                analysis_prompt = f"""Analiza esta conversación con un cliente y extrae:

1. Idea principal del proyecto
2. Funcionalidades clave mencionadas
3. Objetivos del negocio
4. Puntos de dolor que resuelve
5. Fases de implementación sugeridas

Conversación:
{conversation_text}

Crea un documento de propuesta profesional en Markdown con esta estructura:

# Propuesta - [Título del proyecto]

**Preparado para:** Cliente

**Preparado por:** Chuchurex - Desarrollo Web

**Fecha:** {datetime.now().strftime("%d de %B %Y")}

**Contacto:** carlos@chuchurex.cl

---

## Tu idea en resumen

[Descripción clara de lo que el cliente quiere lograr]

### Cómo funciona

[Lista las características principales, una por línea con espacio entre ellas]

---

## Lo que hace única tu propuesta

[Puntos diferenciadores]

---

## Plataforma digital propuesta

[Desglose de componentes técnicos necesarios]

---

## Próximos pasos sugeridos

### Fase 1: [Nombre]
[Descripción]

### Fase 2: [Nombre]
[Descripción]

---

## Siguiente paso

Agendemos una videollamada de 30 minutos para:
- Mostrarte ejemplos visuales de cómo se vería
- Resolver todas tus dudas
- Definir por dónde empezar

**Contacto:** carlos@chuchurex.cl

---

*Este documento es una propuesta inicial basada en la conversación. Los detalles y funcionalidades pueden ajustarse según tus necesidades específicas.*
"""

                analysis_response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": analysis_prompt}]
                )

                proposal_md = analysis_response.content[0].text

                # Guardar Markdown
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(proposal_md)

                # Generar PDF
                import subprocess
                result = subprocess.run(
                    ["node", f"{PDF_GENERATOR_DIR}/generate-pdf-api.js", md_path, pdf_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    # PDF generado exitosamente
                    pdf_filename = f"{filename_base}.pdf"
                    # Remover el trigger de la respuesta
                    clean_response = response_text.replace("[PDF_TRIGGER]", "").strip()
                    return ChatResponse(
                        response=clean_response,
                        generate_pdf=True,
                        pdf_url=f"/download-proposal/{pdf_filename}"
                    )
            except Exception as e:
                # Si falla, responder normalmente sin PDF (removiendo el trigger)
                response_text = response_text.replace("[PDF_TRIGGER]", "").strip()

        return ChatResponse(response=response_text)
    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail="Error communicating with AI service")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/download-proposal/{filename}")
async def download_proposal(filename: str):
    """Descarga una propuesta PDF generada"""
    try:
        pdf_path = f"{PROPOSALS_DIR}/{filename}"
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="Propuesta no encontrada")

        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=filename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descargando propuesta: {str(e)}")

class ProposalRequest(BaseModel):
    client_name: str
    project_summary: str
    conversation_history: List[Message]

@app.post("/generate-proposal")
async def generate_proposal(request: ProposalRequest):
    """Genera una propuesta en PDF basada en la conversación del chat"""
    try:
        # Generar nombre único para la propuesta
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"propuesta_{request.client_name.lower().replace(' ', '_')}_{timestamp}"
        md_path = f"{PROPOSALS_DIR}/{filename_base}.md"
        pdf_path = f"{PROPOSALS_DIR}/{filename_base}.pdf"
        
        # Extraer información clave de la conversación usando Claude
        conversation_text = "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in request.conversation_history
        ])
        
        analysis_prompt = f"""Analiza esta conversación con un cliente y extrae:

1. Idea principal del proyecto
2. Funcionalidades clave mencionadas
3. Objetivos del negocio
4. Puntos de dolor que resuelve
5. Fases de implementación sugeridas

Conversación:
{conversation_text}

Crea un documento de propuesta profesional en Markdown con esta estructura:

# Propuesta - [Título del proyecto]

**Preparado para:** {request.client_name}

**Preparado por:** Chuchurex - Desarrollo Web

**Fecha:** {datetime.now().strftime("%d de %B %Y")}

**Contacto:** carlos@chuchurex.cl

---

## Tu idea en resumen

[Descripción clara de lo que el cliente quiere lograr]

### Cómo funciona

[Lista las características principales, una por línea con espacio entre ellas]

---

## Lo que hace única tu propuesta

[Puntos diferenciadores]

---

## Plataforma digital propuesta

[Desglose de componentes técnicos necesarios]

---

## Próximos pasos sugeridos

### Fase 1: [Nombre]
[Descripción]

### Fase 2: [Nombre]
[Descripción]

---

## Siguiente paso

Agendemos una videollamada de 30 minutos para:
- Mostrarte ejemplos visuales de cómo se vería
- Resolver todas tus dudas
- Definir por dónde empezar

**Contacto:** carlos@chuchurex.cl

---

*Este documento es una propuesta inicial basada en la conversación. Los detalles y funcionalidades pueden ajustarse según tus necesidades específicas.*
"""
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        proposal_md = response.content[0].text
        
        # Guardar Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(proposal_md)
        
        # Generar PDF usando Node.js
        result = subprocess.run(
            ["node", f"{PDF_GENERATOR_DIR}/generate-pdf-api.js", md_path, pdf_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {result.stderr}")
        
        # Retornar el PDF
        return FileResponse(
            path=pdf_path,
            media_type="application/pdf",
            filename=f"propuesta_{request.client_name.replace(' ', '_')}.pdf"
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="PDF generation timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating proposal: {str(e)}")
