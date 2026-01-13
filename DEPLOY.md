# Chuchurex Deploy

## 🤖 INSTRUCTIONS FOR CLAUDE CODE

**IMPORTANT:** This document is for Claude Code to deploy automatically without asking every time.

### Frontend Deploy (ALWAYS USE THIS METHOD)

When modifying frontend files (`frontend/` directory), deploy is **automatic via GitHub**:

```bash
# 1. Stage modified files
git add frontend/

# 2. Commit with descriptive message
git commit -m "change description"

# 3. Push to GitHub (Cloudflare Pages detects and deploys automatically)
git push origin main
```

**DON'T TRY:** rsync, scp, ssh to server directly - that server is only for backend API.

**HOSTING:** Cloudflare Pages detects the push and deploys automatically in ~1 minute.

---

## Architecture

The project has two separate parts:

| Component | Hosting | Deploy |
|-----------|---------|--------|
| **Frontend** | Cloudflare Pages | Auto-deploy from GitHub |
| **Backend API** | Vultr VPS | Manual with `./deploy.sh` |

---

## Frontend (chuchurex.cl)

### Hosting: Cloudflare Pages

Frontend is directly connected to GitHub. **Does NOT use Hostinger**.

### Automatic deploy

Just push to GitHub:

```bash
git add .
git commit -m "your message"
git push origin main
```

Cloudflare Pages detects the push and deploys automatically in ~1 minute.

### Verify deploy

- Production: https://chuchurex.cl
- About: https://chuchurex.cl/about.html
- Privacy: https://chuchurex.cl/privacidad.html

### Cloudflare configuration

- **Project:** chuchurex
- **Branch:** main
- **Build command:** (none, static files)
- **Output directory:** frontend

---

## Backend API (api.chuchurex.cl)

### Hosting: Vultr VPS

Server details are in `.env` (VPS_HOST, VPS_USER, VPS_PATH).

### 🤖 Deploy for Claude Code

When modifying backend files (`app.py`, `app_unified.py`, `pdf-generator/`):

```bash
# The deploy.sh script handles SSH automatically
./deploy.sh
```

**YOU DON'T NEED:** Configure SSH, add keys, or run rsync/scp manually. The `deploy.sh` script has everything configured.

### Manual deploy (humans)

```bash
./deploy.sh
```

This script:
1. Uploads `app_unified.py` as `app.py`
2. Uploads `pdf-generator/`
3. Installs Node dependencies
4. Restarts `chuchurex` service

### Verify API

- API: https://api.chuchurex.cl
- Health check: https://api.chuchurex.cl/health
- Chats: https://api.chuchurex.cl/chats?key=${CHATS_ACCESS_KEY}

---

## Local Development

### Start frontend

```bash
npm run dev
```

Automatically opens http://localhost:3007

### Available scripts

```bash
npm run dev          # Frontend with live-reload + opens browser
npm run dev:frontend # Frontend without opening browser
npm run dev:backend  # Backend (requires venv with uvicorn)
```

---

## Quick Summary

```bash
# Development
npm run dev

# Publish frontend (auto)
git add . && git commit -m "message" && git push

# Publish backend (manual)
./deploy.sh
```

---

## 🤖 Checklist for Claude Code

### Before deploying frontend:
- [ ] Did I modify files in `frontend/`? → Use git push (NOT ssh/rsync)
- [ ] Stage files: `git add frontend/`
- [ ] Commit: `git commit -m "description"`
- [ ] Push: `git push origin main`
- [ ] Cloudflare Pages deploys automatically in ~1 min

### Before deploying backend:
- [ ] Did I modify `app.py`, `app_unified.py` or `pdf-generator/`?
- [ ] Execute: `./deploy.sh`
- [ ] Script handles SSH automatically

### ⚠️ NEVER DO:
- ❌ `rsync frontend/` to VPS server
- ❌ `scp frontend/*.html` to VPS server
- ❌ SSH to VPS to upload frontend
- ❌ Ask for SSH keys for frontend deploy

### ✅ ALWAYS DO:
- ✅ Frontend → git push origin main
- ✅ Backend → ./deploy.sh
- ✅ Read this file before attempting deploy

---

## Notes

- **DO NOT use Hostinger** for this project
- The `deploy-frontend.sh` file is obsolete (was for Hostinger)
- Cloudflare Pages does automatic deploy, you don't need wrangler
- VPS server is **ONLY for backend API**, not for frontend
