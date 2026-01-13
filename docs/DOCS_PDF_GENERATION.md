# Sistema de Generación Automática de Propuestas en PDF

## Descripción General

Sistema que analiza conversaciones del chatbot con clientes y genera automáticamente propuestas profesionales en PDF, usando IA para extraer información clave y crear documentos estructurados.

## Arquitectura

```
┌─────────────────┐
│   Usuario       │
│   (Frontend)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│          FastAPI Backend                    │
│  ┌──────────────────────────────────────┐  │
│  │  /chat Endpoint                      │  │
│  │  - Detecta [PDF_TRIGGER]             │  │
│  │  - Analiza conversación con Sonnet   │  │
│  │  - Genera Markdown                   │  │
│  │  - Llama a Node.js para PDF          │  │
│  └──────────────┬───────────────────────┘  │
│                 │                           │
│  ┌──────────────▼───────────────────────┐  │
│  │  /download-proposal/{filename}       │  │
│  │  - Sirve el PDF generado             │  │
│  └──────────────────────────────────────┘  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Node.js         │
         │  Puppeteer       │
         │  (PDF Generator) │
         └─────────────────┘
```

## Componentes del Sistema

### 1. Backend (FastAPI) - `/app.py`

#### Detección Inteligente

El chatbot ofrece generar propuesta cuando detecta:

**Opción A - VOLUMEN:**
- 6+ mensajes intercambiados
- Usuario ha explicado su idea con detalle

**Opción B - PALABRAS CLAVE:**
- "presupuesto", "cuánto cuesta", "cotización", "precio", "contratar"

**Opción C - PRÓXIMOS PASOS:**
- "qué sigue", "cómo seguimos", "próximos pasos"

#### System Prompt

```python
PROPUESTA EN PDF - DETECCIÓN INTELIGENTE:

CUÁNDO OFRECER la propuesta en PDF:
"¿Te gustaría que te prepare un documento con todo lo que hemos conversado? Te puedo generar un PDF."

CUÁNDO ACTIVAR el PDF (DEBES incluir [PDF_TRIGGER]):
- Si el usuario ACEPTA tu oferta (dice "sí", "dale", "perfecto", "quiero", etc.)
- Si el usuario PIDE directamente una propuesta/cotización/documento desde el inicio

CRÍTICO - Respuestas correctas:
- "Perfecto. [PDF_TRIGGER]"
- "Dale. [PDF_TRIGGER]"
- "Excelente. [PDF_TRIGGER]"
- "Listo. [PDF_TRIGGER]"
```

#### Flujo de Generación

```python
# 1. Detectar trigger
if "[PDF_TRIGGER]" in response_text:

    # 2. Analizar conversación con Claude Sonnet
    analysis_response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": analysis_prompt}]
    )

    # 3. Guardar Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(proposal_md)

    # 4. Generar PDF con Node.js
    result = subprocess.run(
        ["node", f"{PDF_GENERATOR_DIR}/generate-pdf-api.js", md_path, pdf_path],
        capture_output=True,
        text=True,
        timeout=30
    )

    # 5. Retornar URL de descarga
    return ChatResponse(
        response=clean_response,
        generate_pdf=True,
        pdf_url=f"/download-proposal/{pdf_filename}"
    )
```

#### Template de Análisis

El prompt para Claude Sonnet extrae:
1. Idea principal del proyecto
2. Funcionalidades clave mencionadas
3. Objetivos del negocio
4. Puntos de dolor que resuelve
5. Fases de implementación sugeridas

### 2. Generador PDF (Node.js) - `/pdf-generator/generate-pdf-api.js`

#### Dependencias

```json
{
  "devDependencies": {
    "puppeteer": "^23.11.1",
    "markdown-it": "^14.1.0"
  }
}
```

#### Proceso

```javascript
async function generatePDF(mdFilePath, outputPdfPath) {
    // 1. Leer Markdown
    const mdContent = fs.readFileSync(mdFilePath, 'utf-8');

    // 2. Convertir a HTML
    const htmlBody = md.render(mdContent);

    // 3. Aplicar estilos CSS
    const fullHtml = `<!DOCTYPE html>
    <html lang="es">
    <head>
        <style>
            /* Estilos Chuchurex */
        </style>
    </head>
    <body>
        <div class="header-logo">Chuchurex</div>
        ${htmlBody}
        <div class="footer-url">https://chuchurex.cl/</div>
    </body>
    </html>`;

    // 4. Generar PDF con Puppeteer
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();
    await page.setContent(fullHtml, { waitUntil: 'networkidle0' });

    await page.pdf({
        path: outputPdfPath,
        format: 'A4',
        printBackground: true,
        margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' }
    });

    await browser.close();
}
```

#### Estilos del PDF

- **Logo:** "Chuchurex" en esquina superior izquierda (solo primera página)
- **Color:** Negro (#000) para texto, conchevino (#722F37) para logo
- **Tipografía:**
  - Cuerpo: 14px, justify
  - H1: 24px
  - H2: 20px
  - H3: 18px
- **Márgenes:** 20mm en todos los lados
- **Footer:** URL al final del documento

### 3. Frontend (JavaScript) - `/frontend/js/app.js`

#### Flujo UX

```javascript
// 1. Usuario acepta propuesta
const data = await response.json();

// 2. Mostrar respuesta del bot (ej: "Perfecto.")
displayMessage(data.response, 'assistant');

// 3. Mostrar indicador de carga
if (data.generate_pdf && data.pdf_url) {
    const loadingIndicator = displayPDFLoadingIndicator();
    // 🔄 "Generando tu propuesta..."

    // 4. Después de 3 segundos, mostrar botón de descarga
    setTimeout(() => {
        loadingIndicator.remove();
        displayPDFDownloadLink(data.pdf_url);
        // ✅ "Tu propuesta está lista [Descargar Propuesta PDF]"
    }, 3000);
}
```

#### Componentes Visuales

**Indicador de Carga:**
```html
<div class="message-pdf-loading">
    <div class="pdf-loading-content">
        <div class="pdf-spinner"></div>
        <p>Generando tu propuesta...</p>
    </div>
</div>
```

**Botón de Descarga:**
```html
<div class="message-pdf">
    <p>✅ <strong>Tu propuesta está lista</strong></p>
    <a href="/api/download-proposal/propuesta_cliente_20260106_092150.pdf"
       class="pdf-download-button"
       target="_blank"
       download>
        <svg>...</svg>
        Descargar Propuesta PDF
    </a>
</div>
```

### 4. Estilos (CSS) - `/frontend/styles/main.css`

```css
/* Indicador de carga */
.message-pdf-loading {
    border-left: 3px solid var(--color-conchevino-light);
    padding-left: var(--spacing-md);
}

.pdf-spinner {
    width: 20px;
    height: 20px;
    border: 3px solid var(--color-crema-dark);
    border-top-color: var(--color-conchevino);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

/* Botón de descarga */
.pdf-download-button {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--color-conchevino);
    color: var(--color-white);
    border-radius: var(--radius-sm);
    transition: all var(--transition);
    box-shadow: var(--shadow-sm);
}

.pdf-download-button:hover {
    background: var(--color-conchevino-dark);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}
```

## Estructura de Directorios

```
/var/www/chuchurex-api/
├── app.py                          # FastAPI backend
├── chats/                          # Conversaciones guardadas
│   └── chat_YYYYMMDD_HHMMSS.json
├── pdf-generator/                  # Generador Node.js
│   ├── package.json
│   ├── package-lock.json
│   ├── node_modules/
│   ├── generate-pdf-api.js         # Script principal
│   └── generate-pdf.js             # Script de testing
└── proposals/                      # PDFs generados
    ├── propuesta_cliente_YYYYMMDD_HHMMSS.md
    └── propuesta_cliente_YYYYMMDD_HHMMSS.pdf
```

## Estructura del PDF Generado

```markdown
# Propuesta - [Título del proyecto]

**Preparado para:** Cliente

**Preparado por:** Chuchurex - Desarrollo Web

**Fecha:** 6 de enero 2026

**Contacto:** carlos@chuchurex.cl

---

## Tu idea en resumen

[Descripción clara de lo que el cliente quiere lograr]

### Cómo funciona

[Características principales, una por línea]

---

## Lo que hace única tu propuesta

[Puntos diferenciadores]

---

## Plataforma digital propuesta

[Componentes técnicos necesarios]

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
```

## Instalación y Configuración

### 1. Servidor (VPS Ubuntu 24.04)

```bash
# Instalar Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Instalar dependencias de Chrome para Puppeteer
apt-get install -y \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
  libxfixes3 libxrandr2 libgbm1 libasound2t64 \
  libpango-1.0-0 libcairo2 libatspi2.0-0

# Crear directorios
mkdir -p /var/www/chuchurex-api/pdf-generator
mkdir -p /var/www/chuchurex-api/proposals

# Instalar dependencias npm
cd /var/www/chuchurex-api/pdf-generator
npm install --save-dev puppeteer markdown-it

# Reiniciar servicio
systemctl restart chuchurex
```

### 2. Variables de Entorno

```bash
# /var/www/chuchurex-api/.env
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

### 3. Configuración de Servicio

```ini
# /etc/systemd/system/chuchurex.service
[Unit]
Description=Chuchurex API
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/chuchurex-api
Environment="PATH=/var/www/chuchurex-api/venv/bin:/usr/local/bin:/usr/bin"
ExecStart=/var/www/chuchurex-api/venv/bin/uvicorn app:app --host 127.0.0.1 --port 8002
Restart=always

[Install]
WantedBy=multi-user.target
```

## Endpoints de la API

### POST `/chat`

**Request:**
```json
{
  "message": "Quiero modernizar mi sitio web",
  "history": []
}
```

**Response (normal):**
```json
{
  "response": "Hola, perfecto. Cuéntame más sobre tu proyecto...",
  "generate_pdf": false,
  "pdf_url": null
}
```

**Response (con PDF):**
```json
{
  "response": "Perfecto.",
  "generate_pdf": true,
  "pdf_url": "/download-proposal/propuesta_cliente_20260106_092150.pdf"
}
```

### GET `/download-proposal/{filename}`

**Response:**
- Content-Type: `application/pdf`
- Content-Disposition: `attachment; filename="propuesta_cliente_20260106_092150.pdf"`

### GET `/chats?key=${CHATS_ACCESS_KEY}`

Vista HTML de todas las conversaciones guardadas durante la fase beta.

## Ejemplos de Uso

### Caso 1: Usuario pide propuesta directamente

```
Usuario: "Quiero modernizar kiligcoffee.cl, necesito una propuesta"
Bot: "Hola, perfecto." [PDF_TRIGGER]
Sistema: 🔄 "Generando tu propuesta..."
Sistema: ✅ [Botón descargar PDF]
```

### Caso 2: Bot ofrece después de conversación

```
Usuario: "Quiero crear una app de delivery"
Bot: "Cuéntame más sobre tu idea..."
[... 6+ mensajes ...]
Bot: "¿Te gustaría que te prepare un documento con todo lo conversado? Te puedo generar un PDF."
Usuario: "sí"
Bot: "Dale." [PDF_TRIGGER]
Sistema: 🔄 "Generando tu propuesta..."
Sistema: ✅ [Botón descargar PDF]
```

### Caso 3: Usuario menciona presupuesto

```
Usuario: "Cuánto cuesta hacer una landing page?"
Bot: "Para una landing page el rango es -300 USD. ¿Te gustaría que te prepare un documento con lo que hemos conversado? Te puedo generar un PDF."
Usuario: "dale"
Bot: "Listo." [PDF_TRIGGER]
Sistema: 🔄 "Generando tu propuesta..."
Sistema: ✅ [Botón descargar PDF]
```

## Calibración del Algoritmo

El sistema usa tres estrategias (A, B, C) que se pueden calibrar:

**Ajustar umbral de mensajes:**
```python
# Cambiar de 6+ a otro número
A) VOLUMEN: Han intercambiado 8+ mensajes Y el usuario ha explicado su idea
```

**Agregar más keywords:**
```python
B) PALABRAS CLAVE: El usuario menciona "presupuesto", "cuánto cuesta",
   "cotización", "precio", "contratar", "tarifas", "inversión"
```

**Monitoreo:**
```bash
# Ver conversaciones y evaluar cuándo ofreció PDF
curl "https://api.chuchurex.cl/chats?key=\${CHATS_ACCESS_KEY}"
```

## Logs y Debugging

### Ver logs del servicio
```bash
journalctl -u chuchurex -f
```

### Test manual de PDF
```bash
cd /var/www/chuchurex-api/pdf-generator
node generate-pdf.js
```

### Verificar PDFs generados
```bash
ls -lh /var/www/chuchurex-api/proposals/
```

## Limitaciones Conocidas

1. **Timeout:** PDFs grandes pueden tardar más de 30 segundos
2. **Concurrencia:** Sin cola de procesamiento, requests simultáneos pueden sobresaturar
3. **Almacenamiento:** PDFs no se eliminan automáticamente
4. **Nombre genérico:** PDFs usan "Cliente" en vez del nombre real del usuario
5. **Sin email:** PDFs solo se descargan, no se envían por email

## Mejoras Futuras

- [ ] Pedir nombre al usuario antes de generar PDF
- [ ] Envío automático por email
- [ ] Cola de procesamiento (Redis/Celery)
- [ ] Limpieza automática de PDFs antiguos (>30 días)
- [ ] Soporte para múltiples templates según tipo de proyecto
- [ ] Versión imprimible vs. versión digital optimizada
- [ ] Analytics: rastrear cuántos PDFs se generan y descargan
- [ ] Preview del PDF antes de descargar
- [ ] Permitir edición de propuesta antes de generar PDF final

## Troubleshooting

### Error: "Chrome not found"
```bash
# Reinstalar dependencias de Chrome
apt-get install --reinstall chromium-browser
```

### Error: "Failed to launch browser"
```bash
# Verificar flags de sandbox
grep "no-sandbox" /var/www/chuchurex-api/pdf-generator/generate-pdf-api.js
```

### PDF no se descarga
```bash
# Verificar permisos
chmod 755 /var/www/chuchurex-api/proposals/
ls -la /var/www/chuchurex-api/proposals/
```

### Trigger no detectado
```bash
# Revisar logs del chat
tail -f /var/www/chuchurex-api/chats/chat_*.json
# Buscar si incluye [PDF_TRIGGER]
```

## Referencias

- [Puppeteer Documentation](https://pptr.dev/)
- [markdown-it](https://github.com/markdown-it/markdown-it)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Claude API](https://docs.anthropic.com/)

---

**Última actualización:** 6 de enero 2026
**Versión:** 1.0
**Autor:** Carlos / Chuchurex + Claude Sonnet 4.5
