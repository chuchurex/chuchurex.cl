# Deploy de Chuchurex

## 🤖 INSTRUCCIONES PARA CLAUDE CODE

**IMPORTANTE:** Este documento es para que Claude Code pueda deployar automáticamente sin preguntar cada vez.

### Deploy Frontend (SIEMPRE USA ESTE MÉTODO)

Cuando modifiques archivos del frontend (`frontend/` directory), el deploy es **automático vía GitHub**:

```bash
# 1. Stage los archivos modificados
git add frontend/

# 2. Commit con mensaje descriptivo
git commit -m "descripción del cambio"

# 3. Push a GitHub (Cloudflare Pages detecta y despliega automáticamente)
git push origin main
```

**NO INTENTAR:** rsync, scp, ssh al servidor 64.176.19.44 - ese servidor es solo para el backend API.

**HOSTING:** Cloudflare Pages detecta el push y despliega en ~1 minuto automáticamente.

---

## Arquitectura

El proyecto tiene dos partes separadas:

| Componente | Hosting | Deploy |
|------------|---------|--------|
| **Frontend** | Cloudflare Pages | Auto-deploy desde GitHub |
| **Backend API** | Vultr VPS (64.176.19.44) | Manual con `./deploy.sh` |

---

## Frontend (chuchurex.cl)

### Hosting: Cloudflare Pages

El frontend está conectado directamente a GitHub. **No usa Hostinger**.

### Deploy automático

Solo necesitas hacer push a GitHub:

```bash
git add .
git commit -m "tu mensaje"
git push origin main
```

Cloudflare Pages detecta el push y despliega automáticamente en ~1 minuto.

### Verificar deploy

- Producción: https://chuchurex.cl
- About: https://chuchurex.cl/about.html
- Privacidad: https://chuchurex.cl/privacidad.html

### Configuración en Cloudflare

- **Proyecto:** chuchurex
- **Branch:** main
- **Build command:** (ninguno, archivos estáticos)
- **Output directory:** frontend

---

## Backend API (api.chuchurex.cl)

### Hosting: Vultr VPS

```
IP: 64.176.19.44
Usuario: root
Directorio: /var/www/chuchurex-api
```

### 🤖 Deploy para Claude Code

Cuando modifiques archivos del backend (`app.py`, `app_unified.py`, `pdf-generator/`):

```bash
# El script deploy.sh maneja SSH automáticamente
./deploy.sh
```

**NO NECESITAS:** Configurar SSH, agregar claves, o ejecutar rsync/scp manualmente. El script `deploy.sh` ya tiene todo configurado.

### Deploy manual (humanos)

```bash
./deploy.sh
```

Este script:
1. Sube `app_unified.py` como `app.py`
2. Sube `pdf-generator/`
3. Instala dependencias de Node
4. Reinicia el servicio `chuchurex`

### Verificar API

- API: https://api.chuchurex.cl
- Health check: https://api.chuchurex.cl/health
- Chats: https://api.chuchurex.cl/chats?key=chuchu2026

---

## Desarrollo local

### Levantar frontend

```bash
npm run dev
```

Abre automáticamente http://localhost:3007

### Scripts disponibles

```bash
npm run dev          # Frontend con live-reload + abre navegador
npm run dev:frontend # Frontend sin abrir navegador
npm run dev:backend  # Backend (requiere venv con uvicorn)
```

---

## Resumen rápido

```bash
# Desarrollo
npm run dev

# Publicar frontend (auto)
git add . && git commit -m "mensaje" && git push

# Publicar backend (manual)
./deploy.sh
```

---

## 🤖 Checklist para Claude Code

### Antes de deployar frontend:
- [ ] ¿Modifiqué archivos en `frontend/`? → Usar git push (NO ssh/rsync)
- [ ] Stage archivos: `git add frontend/`
- [ ] Commit: `git commit -m "descripción"`
- [ ] Push: `git push origin main`
- [ ] Cloudflare Pages despliega automáticamente en ~1 min

### Antes de deployar backend:
- [ ] ¿Modifiqué `app.py`, `app_unified.py` o `pdf-generator/`?
- [ ] Ejecutar: `./deploy.sh`
- [ ] El script maneja SSH automáticamente

### ⚠️ NUNCA HACER:
- ❌ `rsync frontend/ root@64.176.19.44:/var/www/...`
- ❌ `scp frontend/*.html root@64.176.19.44:...`
- ❌ `ssh root@64.176.19.44` para subir frontend
- ❌ Preguntar por claves SSH para frontend deploy

### ✅ SIEMPRE HACER:
- ✅ Frontend → git push origin main
- ✅ Backend → ./deploy.sh
- ✅ Leer este archivo antes de intentar deploy

---

## Notas

- **NO usar Hostinger** para este proyecto
- El archivo `deploy-frontend.sh` está obsoleto (era para Hostinger)
- Cloudflare Pages hace el deploy automático, no necesitas wrangler
- El servidor 64.176.19.44 es **SOLO para backend API**, no para frontend
