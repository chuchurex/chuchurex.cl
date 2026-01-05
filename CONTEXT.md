# uman.ia (chuchurex.cl) - Contexto

> **Actualizado:** 5 Enero 2026
> **Estado:** MVP en desarrollo (40%)
> **Fase:** Frontend + Backend funcionales

---

## Resumen

Chatbot de desarrollo web que ayuda a estructurar ideas y generar cotizaciones. Usa Claude API (Haiku) como motor de IA. Diseño minimalista con paleta crema + conchevino.

---

## Estado Actual

- **Fase:** 1/3 - MVP funcional local
- **Progreso:** 40%
- **Último deploy:** N/A (desarrollo local)
- **URL prod:** chuchurex.cl (pendiente)
- **URL local:** http://localhost:3007

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA                             │
└─────────────────────────────────────────────────────────────────┘

Usuario
   │
   ▼
chuchurex.cl (Cloudflare Pages)
   │
   ▼
api.chuchurex.cl/chat (Vultr VPS)
   │ FastAPI
   ▼
Claude API Haiku (Anthropic)
```

---

## Stack

| Capa | Tecnología |
|------|------------|
| Frontend | HTML + CSS + JS vanilla |
| Backend | FastAPI (Python) |
| IA | Claude Haiku API |
| Hosting FE | Cloudflare Pages |
| Hosting BE | Vultr VPS |

---

## Estructura de Archivos

```
uman.ia/
├── frontend/
│   ├── index.html
│   ├── styles/main.css
│   └── js/app.js
├── backend/
│   ├── app.py
│   └── requirements.txt
├── docs/
│   └── ARQUITECTURA.md
├── .env
├── .env.example
├── .gitignore
├── CONTEXT.md
├── TARIFAS.md
├── VISION_HUMAN_IA.md
└── dev.sh
```

---

## Comandos

```bash
# Desarrollo (frontend + backend)
./dev.sh

# Solo frontend
cd frontend && python3 -m http.server 3007

# Solo backend
cd backend && python app.py
```

---

## Puertos

| Puerto | Uso |
|--------|-----|
| 3007 | Frontend local |
| 8002 | Backend local |

---

## Tarifas (ver TARIFAS.md)

| Tipo | Precio USD |
|------|------------|
| Landing | $200-300 |
| Sitio completo | $500-800 |
| Rediseño | $400-600 |
| App simple | $800-1500 |
| App compleja | $1500-3000 |
| CLI | $300-500 |
| Audiolibro | $100 |
| Biblioteca | $500 |

---

## Historial de Cambios

### 2026-01-05 - feat: MVP inicial
- Frontend completo (HTML + CSS + JS)
- Backend con FastAPI + Claude API
- System prompt de Chuchu definido
- Modelo de tarifas establecido
- Archivos: frontend/*, backend/*, TARIFAS.md, dev.sh

### 2026-01-04 - docs: CONTEXT.md
- Creado archivo de contexto estandarizado
- Archivos: CONTEXT.md

### 2025-XX-XX - docs: Visión inicial
- Documento de visión creado
- Archivos: VISION_HUMAN_IA.md

---

## Próximos Pasos

- [ ] Probar chat localmente
- [ ] Ajustar system prompt según feedback
- [ ] Configurar CI/CD (.github/workflows)
- [ ] Deploy frontend a Cloudflare Pages
- [ ] Deploy backend a Vultr VPS
- [ ] Configurar DNS chuchurex.cl

---

*Protocolo de contexto activo - Ver ~/Sites/vigentes/PROTOCOLO-CONTEXTO.md*
