# Chuchurex - Chatbot MVP (Beta)

Chatbot para cotización de proyectos web con IA.

> **Estado: Beta** - Las conversaciones se almacenan para análisis y mejora del sistema.

## URLs de Producción

- **Frontend**: https://chuchurex.cl
- **API**: https://api.chuchurex.cl
- **Repositorio**: https://github.com/chuchurex/chuchurex

## Stack Técnico

### Frontend
- HTML/CSS/JS vanilla
- Hospedado en Cloudflare Pages
- Dominio: chuchurex.cl (Cloudflare DNS)

### Backend
- FastAPI + Python
- Claude API (Haiku)
- Hospedado en Vultr VPS (Ubuntu 24.04)

## Estructura del Proyecto

```
uman.ia/
├── frontend/
│   ├── index.html          # Página principal con chat
│   ├── privacidad.html     # Política de privacidad
│   ├── _redirects          # Configuración Cloudflare Pages
│   ├── styles/
│   │   └── main.css        # Estilos (paleta crema + conchevino)
│   └── js/
│       └── app.js          # Lógica del chat
├── backend/
│   └── app.py              # API FastAPI (referencia local)
└── README.md
```

## Configuración del Servidor (VPS)

### Archivos en el servidor

```
/var/www/chuchurex-api/
├── app.py                  # API principal
├── .env                    # ANTHROPIC_API_KEY
├── chats/                  # Conversaciones guardadas (beta)
└── venv/                   # Entorno virtual Python
```

### Acceder a los chats guardados

Via web: `https://api.chuchurex.cl/chats?key=${CHATS_ACCESS_KEY}`

O via SSH (ver credenciales en `.env`).

### Servicios

- **systemd**: `/etc/systemd/system/chuchurex.service`
- **nginx**: `/etc/nginx/sites-available/chuchurex`
- **SSL**: Let's Encrypt via certbot

### Comandos útiles

```bash
# Conectar al servidor (ver VPS_HOST en .env)
ssh ${VPS_USER}@${VPS_HOST}

# Reiniciar el servicio
sudo systemctl restart chuchurex

# Ver logs
sudo journalctl -u chuchurex -f

# Estado del servicio
sudo systemctl status chuchurex
```

## Configuración del Chat (System Prompt)

El chatbot está configurado con las siguientes características:

### Personalidad
- Amigable y profesional
- Español chileno natural (sin exagerar)
- Lenguaje inclusivo neutral
- Una pregunta a la vez (conversación natural)

### Tarifas
| Servicio | Precio USD |
|----------|------------|
| Landing page | $200-300 |
| Sitio web (5-10 págs) | $500-800 |
| Rediseño | $400-600 |
| App web simple | $800-1500 |
| App web compleja | $1500-3000 |

### Condiciones
- Vigencia cotización: 2 días hábiles
- Pago: 100% al finalizar
- Descuento máximo: 20%

### Tecnologías que ofrecemos
- WordPress y cualquier CMS
- Código custom (HTML/CSS/JS, frameworks)

## Deploy

> **🤖 Para Claude Code:** Lee `.claude-instructions.md` o `DEPLOY.md` para instrucciones detalladas

### Frontend (Cloudflare Pages)
El deploy es automático al hacer push a `main`:

```bash
git add frontend/
git commit -m "descripción del cambio"
git push origin main
```

**Cloudflare Pages despliega automáticamente en ~1 minuto**

### Backend (VPS)
Usar el script de deploy:

```bash
./deploy.sh
```

El script sube archivos vía SSH y reinicia el servicio automáticamente.

**Documentación completa:** Ver `DEPLOY.md`

## Diseño

### Paleta de colores
- **Crema**: #F5F0E6 (fondo)
- **Conchevino**: #722F37 (acentos)
- **Texto**: #4A3C3F

### Tipografías
- **Serif**: Cormorant Garamond (logo, títulos)
- **Sans**: Inter (texto general)

## Contacto

- **Email**: carlos@chuchurex.cl
- **Web**: https://chuchurex.cl
