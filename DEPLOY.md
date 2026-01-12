# Deploy de Chuchurex

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

### Deploy manual

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

## Notas

- **NO usar Hostinger** para este proyecto
- El archivo `deploy-frontend.sh` está obsoleto (era para Hostinger)
- Cloudflare Pages hace el deploy automático, no necesitas wrangler
