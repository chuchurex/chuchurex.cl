"""
CHUCHUREX - Backend API (Unified)
FastAPI + Claude API + PDF Generation
Versión portable: funciona en desarrollo y producción
"""

import os
import json
import random
import subprocess
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import anthropic
from dotenv import load_dotenv

# =============================================================================
# CONFIGURACIÓN PORTABLE
# =============================================================================

load_dotenv()

# Detectar directorio base (donde está este archivo)
BASE_DIR = Path(__file__).resolve().parent

# Directorios relativos al proyecto
CHATS_DIR = BASE_DIR / "chats"
PDF_GENERATOR_DIR = BASE_DIR / "pdf-generator"
PROPOSALS_DIR = BASE_DIR / "proposals"

# Crear directorios si no existen
CHATS_DIR.mkdir(exist_ok=True)
PROPOSALS_DIR.mkdir(exist_ok=True)

# API Key
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Detectar entorno
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

# =============================================================================
# SALUDOS ALEATORIOS (MULTILINGÜE)
# =============================================================================

SALUDOS = {
    "es": {
        "con_pregunta": [
            "Hola, cuéntame qué tienes en mente.",
            "Hola, ¿en qué te puedo ayudar?",
            "Hola, cuéntame tu idea.",
            "Hola, ¿qué proyecto tienes en mente?",
        ],
        "simples": [
            "Hola, perfecto.",
            "Hola, dale.",
            "Hola, genial.",
            "Hola, claro.",
        ]
    },
    "en": {
        "con_pregunta": [
            "Hi, tell me what you have in mind.",
            "Hi, how can I help you?",
            "Hi, tell me about your idea.",
            "Hi, what project do you have in mind?",
        ],
        "simples": [
            "Hi, perfect.",
            "Hi, got it.",
            "Hi, great.",
            "Hi, sure.",
        ]
    },
    "pt": {
        "con_pregunta": [
            "Olá, me conta o que você tem em mente.",
            "Olá, como posso te ajudar?",
            "Olá, me conta sua ideia.",
            "Olá, qual projeto você tem em mente?",
        ],
        "simples": [
            "Olá, perfeito.",
            "Olá, beleza.",
            "Olá, legal.",
            "Olá, claro.",
        ]
    }
}

def get_saludo(user_already_explained=False, lang="es"):
    if lang not in SALUDOS:
        lang = "es"
    if user_already_explained:
        return random.choice(SALUDOS[lang]["simples"])
    return random.choice(SALUDOS[lang]["con_pregunta"])

# =============================================================================
# GUARDAR CHATS
# =============================================================================

def save_chat(messages: list, response: str):
    """Guarda la conversación para análisis durante beta"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = CHATS_DIR / f"chat_{timestamp}.json"
        data = {
            "timestamp": datetime.now().isoformat(),
            "messages": messages,
            "response": response
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando chat: {e}")

# =============================================================================
# SYSTEM PROMPTS (MULTILINGÜE)
# =============================================================================

SYSTEM_PROMPTS = {
    "es": """Trabajas en Chuchurex, desarrollador web freelance en Santiago de Chile.

REGLA CRÍTICA: NUNCA te presentes. No digas "soy parte de", "trabajo en", "soy del equipo", ni nada similar. Solo saluda y pregunta directamente.

PERSONALIDAD:
- Directo, sin rodeos, pero amable
- Saludas SOLO con "Hola" y una pregunta. Nada más.
- Usas "genial", "dale", "perfecto", "claro" de forma natural
- NUNCA uses "súper", "bacán", "cachai", "po" ni chilenismos fuertes
- Simplificas todo, nada de jerga técnica innecesaria
- Aportas a la conversación solo cuando es útil

ESTILO DE RESPUESTA:
- Máximo 2-3 oraciones cortas
- Una sola pregunta por mensaje
- Ve al grano, sin relleno
- Invitas a soñar: "echa a volar tu imaginación", "cuéntame todo lo que sueñas para tu proyecto"

FLUJO DE CONVERSACIÓN:
Turno 1-2: Entender qué quiere y animarlo a contar sus ideas
Turno 3-4: Profundizar en el negocio o proyecto
Turno 5-6: Detalles específicos de funcionalidades
Turno 7+: Si hay suficiente info, ofrecer PDF

Turno actual: {turno}

EJEMPLOS DE TU ESTILO:

Usuario: "Hola, necesito una página web para mi negocio de comida"
Tú: "Hola, me gustaría que eches a volar tu imaginación y me cuentes todas las funcionalidades que sueñas para tu sitio. Yo te ayudo a construirlas."

Usuario: "Quiero vender online"
Tú: "Genial. ¿Ya tienes productos listos o partimos desde cero con el catálogo?"

Usuario: "Es para un restaurante"
Tú: "Dale. ¿Necesitas solo mostrar el menú o también reservas online y delivery?"

LO QUE NUNCA HACES:
- Listas con bullets o guiones
- Más de una pregunta por mensaje
- Ofrecer PDF antes del turno 5
- Decir que eres IA
- Presentarte con nombre ("Soy Juan", "Mi nombre es...")
- Usar "súper", "bacán", "cachai"

OFERTA DE PDF (solo turno 5+):
Frase: "¿Te gustaría que te prepare un documento con todo lo que hemos conversado? Te puedo generar un PDF con la propuesta."
Si acepta, responde: "Dale. [PDF_TRIGGER]"

TARIFAS (solo si preguntan):
Landing page: $200-300 USD | Sitio completo: $500-800 USD | App web: $800-3000 USD

IMPORTANTE: Responde SIEMPRE en el idioma en que te escriben.""",

    "en": """You work at Chuchurex, a freelance web developer based in Santiago, Chile.

CRITICAL RULE: NEVER introduce yourself. Don't say "I'm part of", "I work at", "I'm from the team", or anything similar. Just greet and ask directly.

PERSONALITY:
- Direct, no fluff, but friendly
- Greet ONLY with "Hi" and a question. Nothing more.
- Use "great", "got it", "perfect", "sure" naturally
- Keep it simple, no unnecessary tech jargon
- Add value to the conversation only when useful

RESPONSE STYLE:
- Maximum 2-3 short sentences
- Only one question per message
- Get to the point, no filler
- Encourage them to dream: "let your imagination fly", "tell me everything you dream for your project"

CONVERSATION FLOW:
Turn 1-2: Understand what they want and encourage them to share ideas
Turn 3-4: Dig deeper into the business or project
Turn 5-6: Specific functionality details
Turn 7+: If enough info, offer PDF

Current turn: {turno}

EXAMPLES OF YOUR STYLE:

User: "Hi, I need a website for my food business"
You: "Hi, I'd love for you to let your imagination fly and tell me all the features you dream of for your site. I can help you build them."

User: "I want to sell online"
You: "Great. Do you already have products ready or are we starting from scratch with the catalog?"

User: "It's for a restaurant"
You: "Got it. Do you need just a menu display or also online reservations and delivery?"

WHAT YOU NEVER DO:
- Lists with bullets or dashes
- More than one question per message
- Offer PDF before turn 5
- Say you're AI
- Introduce yourself with a name ("I'm John", "My name is...")

PDF OFFER (turn 5+ only):
Phrase: "Would you like me to prepare a document with everything we've discussed? I can generate a PDF with the proposal."
If they accept, respond: "Sure. [PDF_TRIGGER]"

RATES (only if asked):
Landing page: $200-300 USD | Full website: $500-800 USD | Web app: $800-3000 USD

IMPORTANT: ALWAYS respond in the language they write to you.""",

    "pt": """Você trabalha na Chuchurex, desenvolvedor web freelancer em Santiago do Chile.

REGRA CRÍTICA: NUNCA se apresente. Não diga "faço parte de", "trabalho na", "sou da equipe", nem nada similar. Apenas cumprimente e pergunte diretamente.

PERSONALIDADE:
- Direto, sem enrolação, mas amigável
- Cumprimente APENAS com "Olá" e uma pergunta. Nada mais.
- Use "legal", "beleza", "perfeito", "claro" de forma natural
- Simplifique tudo, nada de jargão técnico desnecessário
- Agregue à conversa só quando útil

ESTILO DE RESPOSTA:
- Máximo 2-3 frases curtas
- Uma única pergunta por mensagem
- Vá direto ao ponto, sem enrolação
- Convide a sonhar: "deixe sua imaginação voar", "me conte tudo que você sonha para seu projeto"

FLUXO DA CONVERSA:
Turno 1-2: Entender o que quer e encorajar a contar ideias
Turno 3-4: Aprofundar no negócio ou projeto
Turno 5-6: Detalhes específicos de funcionalidades
Turno 7+: Se tiver info suficiente, oferecer PDF

Turno atual: {turno}

EXEMPLOS DO SEU ESTILO:

Usuário: "Olá, preciso de um site para meu negócio de comida"
Você: "Olá, gostaria que você deixasse sua imaginação voar e me contasse todas as funcionalidades que sonha para seu site. Eu te ajudo a construir."

Usuário: "Quero vender online"
Você: "Legal. Já tem produtos prontos ou vamos começar do zero com o catálogo?"

Usuário: "É para um restaurante"
Você: "Beleza. Precisa só mostrar o cardápio ou também reservas online e delivery?"

O QUE VOCÊ NUNCA FAZ:
- Listas com bullets ou traços
- Mais de uma pergunta por mensagem
- Oferecer PDF antes do turno 5
- Dizer que é IA
- Se apresentar com nome ("Sou João", "Meu nome é...")

OFERTA DE PDF (só turno 5+):
Frase: "Gostaria que eu preparasse um documento com tudo que conversamos? Posso gerar um PDF com a proposta."
Se aceitar, responda: "Claro. [PDF_TRIGGER]"

PREÇOS (só se perguntarem):
Landing page: $200-300 USD | Site completo: $500-800 USD | App web: $800-3000 USD

IMPORTANTE: Responda SEMPRE no idioma em que te escrevem."""
}

def get_system_prompt(lang="es"):
    if lang not in SYSTEM_PROMPTS:
        lang = "es"
    return SYSTEM_PROMPTS[lang]

# =============================================================================
# MODELOS PYDANTIC
# =============================================================================

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    lang: Optional[str] = "es"  # es, en, pt

class ChatResponse(BaseModel):
    response: str
    generate_pdf: Optional[bool] = False
    pdf_url: Optional[str] = None

class ProposalRequest(BaseModel):
    client_name: str
    project_summary: str
    conversation_history: List[Message]

# =============================================================================
# FASTAPI APP
# =============================================================================

app = FastAPI(title="Chuchurex API", version="2.0.0")

# CORS - Configuración para desarrollo y producción
allowed_origins = [
    "https://chuchurex.cl",
    "https://www.chuchurex.cl",
]

# Añadir orígenes de desarrollo
if not IS_PRODUCTION:
    allowed_origins.extend([
        "http://localhost:3000",
        "http://localhost:3007",
        "http://localhost:3010",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3007",
        "http://127.0.0.1:3010",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Chuchurex API is running",
        "version": "2.0.0",
        "environment": "production" if IS_PRODUCTION else "development"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/chats", response_class=HTMLResponse)
async def view_chats(key: str = Query(None)):
    """Vista HTML de conversaciones guardadas (para análisis beta)"""
    if key != os.getenv("CHATS_ACCESS_KEY", ""):
        return HTMLResponse("<h1>Acceso denegado</h1>", status_code=403)
    
    chats = []
    try:
        for filename in sorted(os.listdir(CHATS_DIR), reverse=True):
            if filename.endswith(".json"):
                filepath = CHATS_DIR / filename
                with open(filepath, "r", encoding="utf-8") as f:
                    chat_data = json.load(f)
                    chats.append(chat_data)
    except Exception as e:
        print(f"Error leyendo chats: {e}")
    
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
        for chat in chats[:50]:  # Limitar a 50 más recientes
            html += f'<div class="chat"><div class="timestamp">{chat.get("timestamp", "Sin fecha")}</div>'
            for msg in chat.get("messages", []):
                role_class = "user" if msg["role"] == "user" else "assistant"
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                html += f'<div class="message {role_class}">{content}</div>'
            response = chat.get("response", "").replace("<", "&lt;").replace(">", "&gt;")
            html += f'<div class="message assistant">{response}</div>'
            html += '</div>'
    
    html += "</body></html>"
    return HTMLResponse(html)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal del chat"""
    try:
        messages = []
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})
        if not messages or messages[-1]["content"] != request.message:
            messages.append({"role": "user", "content": request.message})

        # Calcular turno de conversación (cada par user+assistant = 1 turno)
        turno = len(request.history) // 2 + 1
        
        # Detectar idioma del MENSAJE del usuario (no del navegador)
        def detect_message_language(text):
            text_lower = text.lower()
            # Palabras comunes en cada idioma
            en_words = ["hello", "hi", "hey", "need", "want", "would", "like", "please", "website", "help", "looking", "for", "the", "and", "with", "can", "you"]
            pt_words = ["olá", "oi", "preciso", "quero", "gostaria", "por favor", "site", "ajuda", "procuro", "para", "com", "você", "pode"]

            en_count = sum(1 for word in en_words if word in text_lower)
            pt_count = sum(1 for word in pt_words if word in text_lower)

            if en_count > pt_count and en_count > 0:
                return "en"
            elif pt_count > en_count and pt_count > 0:
                return "pt"
            return "es"

        # Usar idioma del mensaje, no del navegador
        lang = detect_message_language(request.message)

        # Detectar si el primer mensaje del usuario ya explica su proyecto
        user_already_explained = False
        if len(messages) == 1:
            first_msg = messages[0]["content"].lower()
            palabra_count = len(first_msg.split())
            # Keywords en los 3 idiomas
            keywords_es = ["quiero", "necesito", "modernizar", "rediseñ", "crear", "hacer", "mejorar", "website", "sitio", "web", "página", "app", "plataforma", "sistema", "busco", "cotizar"]
            keywords_en = ["want", "need", "modernize", "redesign", "create", "make", "improve", "website", "site", "web", "page", "app", "platform", "system", "looking", "quote"]
            keywords_pt = ["quero", "preciso", "modernizar", "redesenhar", "criar", "fazer", "melhorar", "website", "site", "web", "página", "app", "plataforma", "sistema", "procuro", "orçamento"]
            keywords = keywords_es + keywords_en + keywords_pt
            tiene_keyword = any(kw in first_msg for kw in keywords)
            # Si tiene keyword y más de 3 palabras, o si es muy largo (>15 palabras)
            if (palabra_count > 3 and tiene_keyword) or palabra_count > 15:
                user_already_explained = True

        # Inyectar número de turno en el prompt del idioma correspondiente
        current_prompt = get_system_prompt(lang).replace("{turno}", str(turno))

        # Detectar si el usuario está ACEPTANDO una oferta de PDF
        should_generate_pdf = False
        last_bot_msg = ""
        
        # Buscar el último mensaje del bot en el historial
        if request.history:
            for msg in reversed(request.history):
                if msg.role == "assistant":
                    last_bot_msg = msg.content.lower()
                    break
        
        current_user_msg = request.message.lower().strip()
        
        # Si el bot ofreció PDF y el usuario acepta (keywords en los 3 idiomas)
        pdf_offer_keywords = [
            # Español
            "generar un pdf", "preparar un documento", "te puedo generar", "documento con todo",
            # Inglés
            "generate a pdf", "prepare a document", "i can generate", "document with everything",
            # Portugués
            "gerar um pdf", "preparar um documento", "posso gerar", "documento com tudo"
        ]
        user_accepts = [
            # Español
            "sí", "si", "dale", "claro", "ok", "bueno", "perfecto", "va", "vamos",
            "quiero", "porfa", "por favor", "obvio", "ya", "sale", "órale", "venga",
            # Inglés
            "yes", "sure", "okay", "great", "please", "go ahead", "sounds good", "let's do it",
            # Portugués
            "sim", "claro", "ok", "bom", "perfeito", "vamos", "quero", "por favor", "óbvio", "legal"
        ]
        
        bot_offered_pdf = any(kw in last_bot_msg for kw in pdf_offer_keywords)
        user_accepted = any(accept in current_user_msg for accept in user_accepts) and len(current_user_msg) < 50
        
        print(f"[PDF DEBUG] Last bot msg: '{last_bot_msg[:100]}...'")
        print(f"[PDF DEBUG] Current user msg: '{current_user_msg}'")
        print(f"[PDF DEBUG] Bot offered PDF: {bot_offered_pdf}, User accepted: {user_accepted}")
        
        if bot_offered_pdf and user_accepted:
            should_generate_pdf = True
            print("[PDF DEBUG] ✅ Should generate PDF!")

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            system=current_prompt,
            messages=messages
        )
        response_text = response.content[0].text

        save_chat(messages, response_text)

        # Generar PDF si se detectó aceptación O si el modelo incluyó el trigger
        if should_generate_pdf or "[PDF_TRIGGER]" in response_text:
            try:
                pdf_result = await generate_pdf_from_conversation(messages)
                if pdf_result:
                    clean_response = response_text.replace("[PDF_TRIGGER]", "").strip()
                    # Si la respuesta es muy corta, usar una estándar según idioma
                    if len(clean_response) < 3:
                        default_responses = {"es": "Dale.", "en": "Sure.", "pt": "Claro."}
                        clean_response = default_responses.get(lang, "Dale.")
                    return ChatResponse(
                        response=clean_response,
                        generate_pdf=True,
                        pdf_url=pdf_result
                    )
            except Exception as e:
                print(f"Error generando PDF: {e}")
                response_text = response_text.replace("[PDF_TRIGGER]", "").strip()

        return ChatResponse(response=response_text.replace("[PDF_TRIGGER]", "").strip())
    
    except anthropic.APIError as e:
        print(f"Anthropic API error: {e}")
        raise HTTPException(status_code=500, detail="Error communicating with AI service")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def generate_pdf_from_conversation(messages: list) -> Optional[str]:
    """Genera un PDF desde la conversación actual"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"propuesta_cliente_{timestamp}"
        md_path = PROPOSALS_DIR / f"{filename_base}.md"
        pdf_path = PROPOSALS_DIR / f"{filename_base}.pdf"

        # Analizar conversación con Claude Sonnet
        conversation_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        # Fecha en español
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_actual = f"{datetime.now().day} de {meses[datetime.now().month - 1]} {datetime.now().year}"

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

**Fecha:** {fecha_actual}

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
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": analysis_prompt}]
        )

        proposal_md = analysis_response.content[0].text

        # Guardar Markdown
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(proposal_md)

        # Generar PDF con Node.js
        generator_script = PDF_GENERATOR_DIR / "generate-pdf-api.js"
        
        # Usar ruta absoluta de node para compatibilidad con systemd
        node_path = "/usr/bin/node" if IS_PRODUCTION else "node"
        result = subprocess.run(
            [node_path, str(generator_script), str(md_path), str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PDF_GENERATOR_DIR)
        )

        if result.returncode == 0 and pdf_path.exists():
            return f"/download-proposal/{filename_base}.pdf"
        else:
            print(f"Error en generación PDF: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("Timeout generando PDF")
        return None
    except Exception as e:
        print(f"Error generando PDF: {e}")
        return None

@app.get("/download-proposal/{filename}")
async def download_proposal(filename: str):
    """Descarga una propuesta PDF generada"""
    try:
        # Sanitizar filename
        if ".." in filename or "/" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        pdf_path = PROPOSALS_DIR / filename
        if not pdf_path.exists():
            raise HTTPException(status_code=404, detail="Propuesta no encontrada")

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=filename
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error descargando propuesta: {str(e)}")

@app.post("/generate-proposal")
async def generate_proposal(request: ProposalRequest):
    """Genera una propuesta en PDF basada en datos proporcionados"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = request.client_name.lower().replace(" ", "_")[:20]
        filename_base = f"propuesta_{safe_name}_{timestamp}"
        md_path = PROPOSALS_DIR / f"{filename_base}.md"
        pdf_path = PROPOSALS_DIR / f"{filename_base}.pdf"
        
        conversation_text = "\n".join([
            f"{msg.role}: {msg.content}" 
            for msg in request.conversation_history
        ])
        
        meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", 
                 "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        fecha_actual = f"{datetime.now().day} de {meses[datetime.now().month - 1]} {datetime.now().year}"
        
        analysis_prompt = f"""Analiza esta conversación con un cliente y crea una propuesta profesional.

Cliente: {request.client_name}
Resumen: {request.project_summary}

Conversación:
{conversation_text}

Crea un documento de propuesta profesional en Markdown incluyendo:
- Título del proyecto
- Preparado para: {request.client_name}
- Fecha: {fecha_actual}
- Resumen de la idea
- Funcionalidades propuestas
- Fases de implementación
- Próximos pasos
"""
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        proposal_md = response.content[0].text
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(proposal_md)
        
        generator_script = PDF_GENERATOR_DIR / "generate-pdf-api.js"
        node_path = "/usr/bin/node" if IS_PRODUCTION else "node"
        result = subprocess.run(
            [node_path, str(generator_script), str(md_path), str(pdf_path)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PDF_GENERATOR_DIR)
        )
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"PDF generation failed: {result.stderr}")
        
        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=f"propuesta_{request.client_name.replace(' ', '_')}.pdf"
        )
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=500, detail="PDF generation timed out")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating proposal: {str(e)}")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8002))
    uvicorn.run(app, host="0.0.0.0", port=port)
