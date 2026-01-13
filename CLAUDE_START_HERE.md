# 🤖 CLAUDE CODE: LEE ESTO PRIMERO

## Deploy Automático - Chuchurex

### ⚡ Quick Reference

```bash
# Cambios en frontend/ → Git push
git add frontend/
git commit -m "mensaje"
git push origin main

# Cambios en backend → Script deploy
./deploy.sh
```

### 🎯 Regla de Oro

**Frontend = Git push | Backend = ./deploy.sh**

### 📚 Documentación Completa

- **Instrucciones detalladas:** `.claude-instructions.md`
- **Guía completa de deploy:** `DEPLOY.md`
- **Resumen del proyecto:** `README.md`

### ⚠️ Errores Comunes a Evitar

❌ No uses `rsync` o `scp` para frontend
❌ No intentes `ssh root@64.176.19.44` para frontend
❌ No preguntes "¿cómo publico esto?"

✅ Frontend siempre → `git push origin main`
✅ Backend siempre → `./deploy.sh`
✅ Deploy automáticamente cuando el usuario lo pida

### 🚀 Cuando el Usuario Dice:

- "Publica" → Ejecuta el deploy apropiado (git push o ./deploy.sh)
- "Deploy" → Ejecuta el deploy apropiado
- "Sube a producción" → Ejecuta el deploy apropiado

**NO preguntes cómo hacerlo. Ya lo sabes.**

---

**Hosting:**
- Frontend: Cloudflare Pages (auto-deploy desde GitHub)
- Backend: Vultr VPS (deploy.sh maneja SSH)

**Infraestructura diseñada para que deployes automáticamente.**
