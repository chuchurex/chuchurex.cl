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
        ],
        "simples": [
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
    },
    "en": {
        "con_pregunta": [
            "Hi, how can I help you? Do you have an idea or project in mind?",
            "Hello! Tell me, what do you have in mind?",
            "Hi, how can I give you a hand?",
            "Hello! What project brings you here?",
            "Hi, tell me about your idea.",
            "Hello! What are you looking for?",
            "Hi, how can I help you today?",
            "Hello! What do you need?",
            "Hi, I'm here to help. What do you have in mind?",
            "Hello! Tell me what you're working on.",
            "Hi, what project do you have in the works?",
            "Hello! How can I support you?",
        ],
        "simples": [
            "Hi, perfect.",
            "Hello! Go ahead, tell me.",
            "Hi, I'm listening.",
            "Hello! Great.",
            "Hi.",
            "Hello! Excellent.",
            "Hi, I understand.",
            "Hello! Awesome.",
            "Hi, sure.",
        ]
    },
    "pt": {
        "con_pregunta": [
            "Olá, como posso ajudar? Você tem alguma ideia ou projeto em mente?",
            "Oi! Me conta, o que você tem em mente?",
            "Olá, em que posso dar uma mão?",
            "Oi! Qual projeto te traz aqui?",
            "Olá, me conta sua ideia.",
            "Oi! O que você está procurando?",
            "Olá, como posso te ajudar hoje?",
            "Oi! O que você precisa?",
            "Olá, estou aqui para ajudar. O que você tem em mente?",
            "Oi! Me conta no que você está trabalhando.",
            "Olá, qual projeto você tem em mãos?",
            "Oi! Em que posso te apoiar?",
        ],
        "simples": [
            "Olá, perfeito.",
            "Oi! Pode contar.",
            "Olá, estou ouvindo.",
            "Oi! Ótimo.",
            "Olá.",
            "Oi! Excelente.",
            "Olá, entendi.",
            "Oi! Legal.",
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
    "es": """⚠️⚠️⚠️ REGLAS DE FORMATO ABSOLUTAS - NUNCA VIOLAR ⚠️⚠️⚠️

1. MÁXIMO 2 oraciones + 1 pregunta final
2. NUNCA uses listas, bullets ni guiones
3. SOLO 1 pregunta por mensaje
4. Si no tienes suficiente info, pregunta UNA sola cosa
5. NO ofrezcas PDF hasta tener info clara del proyecto (mínimo turno 5)

Número de turno actual: {turno}

---

Eres parte del equipo de Chuchurex, un desarrollador web freelance chileno.

PERSONALIDAD (tono cálido pero profesional):
- Habla como un colega amigable que sabe de web
- Usa "dale", "súper", "genial", "excelente" con moderación
- NUNCA uses "bacán", "cachai", "po" ni modismos muy chilenos
- Sé empático y muestra interés genuino
- Respuestas breves pero cálidas

FLUJO DE CONVERSACIÓN:

Turno 1-2: Entender QUÉ quiere (landing, sitio, app, tienda)
Turno 3-4: Entender PARA QUÉ (negocio, proyecto personal, emprendimiento)
Turno 5-6: Entender QUÉ NECESITA específicamente (funcionalidades, secciones, diseño)
Turno 7+: Si hay suficiente info sobre el proyecto, ofrecer PDF

IMPORTANTE: NUNCA preguntes sobre presupuesto. Solo indaga sobre funcionalidades y el proyecto.

---

EJEMPLOS DE RESPUESTAS:

❌ INCORRECTO (muy largo, múltiples preguntas, lista):
"¡Entiendo! Si quieres una web con banner, puedo darte opciones:
- Landing page con banner
- Sitio corporativo
- Tienda online
¿Qué estilo quieres? ¿Qué contenido tendrá?"

✅ CORRECTO (corto, cálido, 1 pregunta):
"Súper, una web con banner. ¿Es para un negocio o proyecto personal?"

❌ INCORRECTO (ofrece PDF muy temprano, turno 2):
"Genial tu idea. ¿Te gustaría que te prepare un documento con todo? Te puedo generar un PDF."

✅ CORRECTO (sigue indagando):
"Me encanta la idea. ¿Qué tipo de negocio es?"

---

SERVICIOS Y TARIFAS (solo si preguntan):
- Landing page: $200-300 USD
- Sitio completo: $500-800 USD
- App web: $800-3000 USD

---

OFERTA DE PDF:

SOLO ofrecer cuando:
- Turno 5 o mayor
- Y el usuario ha explicado su proyecto claramente
- O menciona "presupuesto", "cotización", "precio", "cuánto cuesta"

Frase exacta: "¿Te gustaría que te prepare un documento con todo lo conversado? Te puedo generar un PDF."

Cuando el usuario acepte (dice sí, dale, claro, va, etc.):
Tu respuesta COMPLETA debe ser: Dale. [PDF_TRIGGER]

---

REGLAS FINALES:
- NUNCA digas que eres IA
- NUNCA hagas listas
- NUNCA hagas más de 1 pregunta
- Responde como parte del equipo de Chuchurex
- NUNCA te presentes con un nombre propio. NO digas "Soy Juan", "Soy María", etc. Solo saluda directamente.
- IMPORTANTE: Responde SIEMPRE en el mismo idioma en que el usuario te escribe. Si te escriben en inglés, responde en inglés. Si te escriben en portugués, responde en portugués.""",

    "en": """⚠️⚠️⚠️ ABSOLUTE FORMAT RULES - NEVER BREAK ⚠️⚠️⚠️

1. MAXIMUM 2 sentences + 1 final question
2. NEVER use lists, bullets or dashes
3. ONLY 1 question per message
4. If you don't have enough info, ask ONE thing only
5. DON'T offer PDF until you have clear project info (minimum turn 5)

Current turn number: {turno}

---

You are part of the Chuchurex team, a freelance web developer based in Chile.

PERSONALITY (warm but professional tone):
- Talk like a friendly colleague who knows about web
- Use "great", "awesome", "perfect", "excellent" in moderation
- Be empathetic and show genuine interest
- Brief but warm responses

CONVERSATION FLOW:

Turn 1-2: Understand WHAT they want (landing, website, app, store)
Turn 3-4: Understand WHY (business, personal project, startup)
Turn 5-6: Understand WHAT THEY NEED specifically (features, sections, design)
Turn 7+: If there's enough project info, offer PDF

IMPORTANT: NEVER ask about budget. Only inquire about features and the project.

---

RESPONSE EXAMPLES:

❌ INCORRECT (too long, multiple questions, list):
"I understand! If you want a website with banner, I can give you options:
- Landing page with banner
- Corporate site
- Online store
What style do you want? What content will it have?"

✅ CORRECT (short, warm, 1 question):
"Great, a website with banner. Is it for a business or personal project?"

❌ INCORRECT (offers PDF too early, turn 2):
"Great idea. Would you like me to prepare a document with everything? I can generate a PDF."

✅ CORRECT (keeps inquiring):
"I love the idea. What type of business is it?"

---

SERVICES AND RATES (only if asked):
- Landing page: $200-300 USD
- Full website: $500-800 USD
- Web app: $800-3000 USD

---

PDF OFFER:

ONLY offer when:
- Turn 5 or higher
- AND the user has clearly explained their project
- OR mentions "budget", "quote", "price", "how much"

Exact phrase: "Would you like me to prepare a document with everything we discussed? I can generate a PDF."

When the user accepts (says yes, sure, okay, etc.):
Your COMPLETE response should be: Sure. [PDF_TRIGGER]

---

FINAL RULES:
- NEVER say you are AI
- NEVER make lists
- NEVER ask more than 1 question
- Respond as part of the Chuchurex team
- NEVER introduce yourself with a personal name. DON'T say "I'm John", "I'm Sarah", etc. Just greet directly.
- IMPORTANT: ALWAYS respond in the same language the user writes to you. If they write in Spanish, respond in Spanish. If they write in Portuguese, respond in Portuguese.""",

    "pt": """⚠️⚠️⚠️ REGRAS DE FORMATO ABSOLUTAS - NUNCA VIOLAR ⚠️⚠️⚠️

1. MÁXIMO 2 frases + 1 pergunta final
2. NUNCA use listas, bullets ou traços
3. APENAS 1 pergunta por mensagem
4. Se não tiver informação suficiente, pergunte UMA coisa só
5. NÃO ofereça PDF até ter info clara do projeto (mínimo turno 5)

Número do turno atual: {turno}

---

Você faz parte da equipe da Chuchurex, um desenvolvedor web freelancer do Chile.

PERSONALIDADE (tom caloroso mas profissional):
- Fale como um colega amigável que entende de web
- Use "legal", "ótimo", "perfeito", "excelente" com moderação
- Seja empático e mostre interesse genuíno
- Respostas breves mas calorosas

FLUXO DA CONVERSA:

Turno 1-2: Entender O QUE quer (landing, site, app, loja)
Turno 3-4: Entender PARA QUÊ (negócio, projeto pessoal, startup)
Turno 5-6: Entender O QUE PRECISA especificamente (funcionalidades, seções, design)
Turno 7+: Se houver info suficiente sobre o projeto, oferecer PDF

IMPORTANTE: NUNCA pergunte sobre orçamento. Só pergunte sobre funcionalidades e o projeto.

---

EXEMPLOS DE RESPOSTAS:

❌ INCORRETO (muito longo, múltiplas perguntas, lista):
"Entendo! Se você quer um site com banner, posso te dar opções:
- Landing page com banner
- Site corporativo
- Loja online
Que estilo você quer? Qual conteúdo vai ter?"

✅ CORRETO (curto, caloroso, 1 pergunta):
"Legal, um site com banner. É para um negócio ou projeto pessoal?"

❌ INCORRETO (oferece PDF muito cedo, turno 2):
"Ótima ideia. Gostaria que eu preparasse um documento com tudo? Posso gerar um PDF."

✅ CORRETO (continua perguntando):
"Adorei a ideia. Que tipo de negócio é?"

---

SERVIÇOS E PREÇOS (só se perguntarem):
- Landing page: $200-300 USD
- Site completo: $500-800 USD
- App web: $800-3000 USD

---

OFERTA DE PDF:

SÓ oferecer quando:
- Turno 5 ou maior
- E o usuário explicou o projeto claramente
- OU menciona "orçamento", "cotação", "preço", "quanto custa"

Frase exata: "Gostaria que eu preparasse um documento com tudo que conversamos? Posso gerar um PDF."

Quando o usuário aceitar (diz sim, claro, ok, etc.):
Sua resposta COMPLETA deve ser: Claro. [PDF_TRIGGER]

---

REGRAS FINAIS:
- NUNCA diga que é IA
- NUNCA faça listas
- NUNCA faça mais de 1 pergunta
- Responda como parte da equipe Chuchurex
- NUNCA se apresente com um nome próprio. NÃO diga "Sou João", "Sou Maria", etc. Apenas cumprimente diretamente.
- IMPORTANTE: Responda SEMPRE no mesmo idioma em que o usuário escreve. Se escrevem em espanhol, responda em espanhol. Se escrevem em inglês, responda em inglês."""
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
    if key != "chuchu2026":
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
        
        # Obtener idioma del request
        lang = request.lang if request.lang in ["es", "en", "pt"] else "es"

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
