# Chuchurex - Project Context

> **Updated:** January 12, 2026
> **Status:** ✅ In production
> **Phase:** Functional MVP with PDF generation

---

## Summary

Web project quotation chatbot that helps structure ideas and generate professional proposals. Uses Claude API (Haiku for chat, Sonnet for PDFs) as AI engine. Minimalist design with cream + burgundy palette.

---

## Current Status

- **Phase:** MVP in production
- **Frontend:** https://chuchurex.cl
- **API:** https://api.chuchurex.cl
- **Active features:**
  - ✅ Conversational chat with Claude Haiku
  - ✅ Automatic PDF proposal generation
  - ✅ Multilingual (ES/EN/PT)
  - ✅ Integrated pricing system

---

## Architecture

```
User
   │
   ▼
chuchurex.cl (Cloudflare Pages)
   │ Frontend HTML/CSS/JS
   ▼
api.chuchurex.cl (Vultr VPS)
   │ FastAPI + Python
   ├─► Claude API Haiku (chat)
   └─► Claude API Sonnet (PDF analysis)
        │
        ▼
   pdf-generator/ (Node.js + Puppeteer)
```

---

## Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | HTML + CSS + JS vanilla |
| Backend | FastAPI (Python) + Node.js |
| AI | Claude API (Haiku + Sonnet) |
| PDFs | Puppeteer + markdown-it |
| Frontend Hosting | Cloudflare Pages |
| Backend Hosting | Vultr VPS (Ubuntu 24.04) |
| DNS | Cloudflare |

---

## File Structure

```
chuchurex.cl/
├── frontend/              # Static frontend
│   ├── index.html         # Main chat
│   ├── about.html         # About page
│   ├── privacidad.html    # Privacy policy
│   ├── js/
│   │   ├── app.js         # Chat logic
│   │   └── i18n.js        # Internationalization
│   └── styles/
│       └── main.css       # Cream + burgundy styles
│
├── pdf-generator/         # PDF generator (Node.js)
│   ├── generate-pdf-api.js
│   └── package.json
│
├── app_unified.py         # Main backend (FastAPI)
├── deploy.sh              # Backend deploy script
├── dev.sh                 # Local development script
│
├── docs/                  # Technical documentation
│   ├── DOCS_PDF_GENERATION.md   # PDF architecture
│   ├── PLAN_PDF_PROPUESTAS.md   # PDF feature plan
│   └── TARIFAS.md               # Pricing model
│
├── .claude-instructions.md      # Claude Code instructions
├── CLAUDE_START_HERE.md         # Deploy quick reference
├── DEPLOY.md                    # Complete deploy guide
├── CONTEXT.md                   # This file
└── README.md                    # Main documentation
```

---

## Deploy

### Frontend
```bash
git add frontend/
git commit -m "description"
git push origin main
```
Cloudflare Pages deploys automatically in ~1 minute.

### Backend
```bash
./deploy.sh
```
Script that uploads `app_unified.py` and `pdf-generator/` to VPS via SSH.

**Complete documentation:** See `DEPLOY.md` and `.claude-instructions.md`

---

## Development Commands

```bash
# Local development (frontend + backend)
npm run dev              # Opens http://localhost:3007

# Frontend only
npm run dev:frontend     # Without auto-opening browser

# Backend only (requires venv)
npm run dev:backend      # Port 8002
```

---

## Ports

| Port | Use |
|--------|-----|
| 3007 | Local frontend |
| 8002 | Local backend |

---

## Additional Documentation

| File | Content |
|---------|-----------|
| `docs/TARIFAS.md` | Pricing model and business terms |
| `docs/DOCS_PDF_GENERATION.md` | PDF system architecture |
| `docs/PLAN_PDF_PROPUESTAS.md` | PDF implementation plan |
| `DEPLOY.md` | Complete deploy guide |
| `.claude-instructions.md` | Claude Code instructions |
| `README.md` | Main project documentation |

---

## Sister Sites

- **Astro Chuchurex:** https://astro.chuchurex.cl (portfolio)
- **El Uno:** https://eluno.org (sister site)

Hreflang SEO tags configured on all pages.

---

## Recent Changes History

### 2026-01-12 - feat: El Uno Menu + SEO
- Added link to eluno.org in menu
- ES/EN/PT translations (El Uno, The One, O Um)
- Hreflang tags for sister sites
- Deploy documentation for Claude Code

### 2026-01-10 - feat: Automatic PDFs
- PDF proposal generation system
- Claude Sonnet integration for analysis
- Puppeteer + markdown-it for rendering

### 2026-01-06 - feat: Automated deploy
- deploy.sh script for backend
- Cloudflare Pages for frontend
- Complete documentation

### 2026-01-05 - feat: Initial MVP
- Complete frontend with i18n
- FastAPI backend + Claude Haiku
- Integrated pricing system

---

## Next Steps

- [ ] Analytics (optional)
- [ ] Automated tests
- [ ] Chat UX improvements
- [ ] More PDF customization options

---

*For deploy information, see `DEPLOY.md` or `.claude-instructions.md`*
