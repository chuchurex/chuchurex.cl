# Chuchurex - Chatbot MVP

Chatbot para cotización de proyectos web con IA.

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
- IP: 64.176.19.44

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
└── venv/                   # Entorno virtual Python
```

### Servicios

- **systemd**: `/etc/systemd/system/chuchurex.service`
- **nginx**: `/etc/nginx/sites-available/chuchurex`
- **SSL**: Let's Encrypt via certbot

### Comandos útiles

```bash
# Conectar al servidor
ssh root@64.176.19.44

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

### Frontend (Cloudflare Pages)
El deploy es automático al hacer push a `main`:

```bash
git add -A
git commit -m "mensaje"
git push
```

### Backend (VPS)
Editar directamente en el servidor y reiniciar:

```bash
ssh root@64.176.19.44
nano /var/www/chuchurex-api/app.py
sudo systemctl restart chuchurex
```

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
