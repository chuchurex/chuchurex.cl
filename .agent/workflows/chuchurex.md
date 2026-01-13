---
description: Desarrollo y despliegue del chatbot Chuchurex con generación de PDF
---

// turbo-all

# Workflow: Chuchurex Development

## Desarrollo Local

1. Iniciar backend local:
```bash
cd /Users/chuchurex/Sites/vigentes/uman.ia && source .venv/bin/activate && uvicorn app_unified:app --reload --port 8002
```

2. Iniciar frontend local:
```bash
cd /Users/chuchurex/Sites/vigentes/uman.ia/frontend && npx live-server --port=3007 --no-browser
```

3. Probar API local:
```bash
curl -s http://127.0.0.1:8002/health
```

## Despliegue a Producción

4. Subir cambios al servidor:
```bash
sshpass -p '@6AqxTjd4.7u3p4+' scp -o StrictHostKeyChecking=no /Users/chuchurex/Sites/vigentes/uman.ia/app_unified.py root@64.176.19.44:/var/www/chuchurex-api/app.py
```

5. Reiniciar servicio en producción:
```bash
sshpass -p '@6AqxTjd4.7u3p4+' ssh -o StrictHostKeyChecking=no root@64.176.19.44 "systemctl restart chuchurex"
```

6. Verificar API en producción:
```bash
curl -s https://api.chuchurex.cl/health
```

7. Ver logs del servidor:
```bash
sshpass -p '@6AqxTjd4.7u3p4+' ssh -o StrictHostKeyChecking=no root@64.176.19.44 "journalctl -u chuchurex -n 30 --no-pager"
```

## Testing

8. Probar chat en producción:
```bash
curl -s -X POST https://api.chuchurex.cl/chat -H "Content-Type: application/json" -d '{"message": "hola", "history": []}'
```
