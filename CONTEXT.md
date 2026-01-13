# Chuchurex - Contexto del Proyecto

> **Actualizado:** 12 Enero 2026
> **Estado:** ✅ En producción
> **Fase:** MVP funcional con generación de PDFs

---

## Resumen

Chatbot de cotización de proyectos web que ayuda a estructurar ideas y generar propuestas profesionales. Usa Claude API (Haiku para chat, Sonnet para PDFs) como motor de IA. Diseño minimalista con paleta crema + conchevino.

---

## Estado Actual

- **Fase:** MVP en producción
- **Frontend:** https://chuchurex.cl
- **API:** https://api.chuchurex.cl
- **Features activas:**
  - ✅ Chat conversacional con Claude Haiku
  - ✅ Generación automática de propuestas en PDF
  - ✅ Multiidioma (ES/EN/PT)
  - ✅ Sistema de tarifas integrado

---

## Arquitectura

```
Usuario
   │
   ▼
chuchurex.cl (Cloudflare Pages)
   │ Frontend HTML/CSS/JS
   ▼
api.chuchurex.cl (Vultr VPS)
   │ FastAPI + Python
   ├─► Claude API Haiku (chat)
   └─► Claude API Sonnet (análisis para PDFs)
        │
        ▼
   pdf-generator/ (Node.js + Puppeteer)
```

---

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | HTML + CSS + JS vanilla |
| Backend | FastAPI (Python) + Node.js |
| IA | Claude API (Haiku + Sonnet) |
| PDFs | Puppeteer + markdown-it |
| Hosting Frontend | Cloudflare Pages |
| Hosting Backend | Vultr VPS (Ubuntu 24.04) |
| DNS | Cloudflare |

---

## Estructura de Archivos

```
chuchurex.cl/
├── frontend/              # Frontend estático
│   ├── index.html         # Chat principal
│   ├── about.html         # Sobre el proyecto
│   ├── privacidad.html    # Política de privacidad
│   ├── js/
│   │   ├── app.js         # Lógica del chat
│   │   └── i18n.js        # Internacionalización
│   └── styles/
│       └── main.css       # Estilos crema + conchevino
│
├── pdf-generator/         # Generador de PDFs (Node.js)
│   ├── generate-pdf-api.js
│   └── package.json
│
├── app_unified.py         # Backend principal (FastAPI)
├── deploy.sh              # Script de deploy backend
├── dev.sh                 # Script desarrollo local
│
├── docs/                  # Documentación técnica
│   ├── DOCS_PDF_GENERATION.md   # Arquitectura PDFs
│   ├── PLAN_PDF_PROPUESTAS.md   # Plan feature PDFs
│   └── TARIFAS.md               # Modelo de precios
│
├── .claude-instructions.md      # Instrucciones para Claude Code
├── CLAUDE_START_HERE.md         # Quick reference deploy
├── DEPLOY.md                    # Guía completa de deploy
├── CONTEXT.md                   # Este archivo
└── README.md                    # Documentación principal
```

---

## Deploy

### Frontend
```bash
git add frontend/
git commit -m "descripción"
git push origin main
```
Cloudflare Pages despliega automáticamente en ~1 minuto.

### Backend
```bash
./deploy.sh
```
Script que sube `app_unified.py` y `pdf-generator/` al VPS vía SSH.

**Documentación completa:** Ver `DEPLOY.md` y `.claude-instructions.md`

---

## Comandos de Desarrollo

```bash
# Desarrollo local (frontend + backend)
npm run dev              # Abre http://localhost:3007

# Solo frontend
npm run dev:frontend     # Sin auto-abrir navegador

# Solo backend (requiere venv)
npm run dev:backend      # Puerto 8002
```

---

## Puertos

| Puerto | Uso |
|--------|-----|
| 3007 | Frontend local |
| 8002 | Backend local |

---

## Documentación Adicional

| Archivo | Contenido |
|---------|-----------|
| `docs/TARIFAS.md` | Modelo de precios y condiciones comerciales |
| `docs/DOCS_PDF_GENERATION.md` | Arquitectura del sistema de PDFs |
| `docs/PLAN_PDF_PROPUESTAS.md` | Plan de implementación de PDFs |
| `DEPLOY.md` | Guía completa de deploy |
| `.claude-instructions.md` | Instrucciones para Claude Code |
| `README.md` | Documentación principal del proyecto |

---

## Sitios Hermanos

- **Astro Chuchurex:** https://astro.chuchurex.cl (portfolio)
- **El Uno:** https://eluno.org (sitio hermano)

Marcas SEO hreflang configuradas en todas las páginas.

---

## Historial de Cambios Recientes

### 2026-01-12 - feat: Menu El Uno + SEO
- Agregado enlace a eluno.org en menú
- Traducciones ES/EN/PT (El Uno, The One, O Um)
- Tags hreflang para sitios hermanos
- Documentación de deploy para Claude Code

### 2026-01-10 - feat: PDFs automáticos
- Sistema de generación de propuestas PDF
- Integración Claude Sonnet para análisis
- Puppeteer + markdown-it para renderizado

### 2026-01-06 - feat: Deploy automatizado
- Script deploy.sh para backend
- Cloudflare Pages para frontend
- Documentación completa

### 2026-01-05 - feat: MVP inicial
- Frontend completo con i18n
- Backend FastAPI + Claude Haiku
- Sistema de tarifas integrado

---

## Próximos Pasos

- [ ] Analytics (opcional)
- [ ] Tests automatizados
- [ ] Mejoras en UX del chat
- [ ] Más opciones de personalización de PDFs

---

*Para información de deploy, ver `DEPLOY.md` o `.claude-instructions.md`*
