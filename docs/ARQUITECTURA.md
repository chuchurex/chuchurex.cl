# Arquitectura - uman.ia (human.ia)

> **Versión:** 0.1 (Borrador)
> **Fecha:** 4 Enero 2026
> **Estado:** IDEA - Solo visión documentada

---

## 1. Visión

Plataforma global de proyectos desarrollados por humanos potenciados con IA.
**Prompt-first:** El usuario escribe su idea → recibe un proyecto desarrollado.

---

## 2. Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARQUITECTURA FUTURA                                 │
└─────────────────────────────────────────────────────────────────────────────┘

   Usuario                                              Controladores IA
      │                                                        │
      │  Escribe prompt                                        │
      ▼                                                        │
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────►│   Backend       │────►│   Dashboard     │
│   (Minimalista) │     │   (FastAPI)     │     │   Controladores │
│   JS + SASS     │     │   PostgreSQL    │     │                 │
│   i18n auto     │     │   Redis         │     │   Asignación    │
│   Solo un input │     │   Claude API    │     │   Tracking      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │                       │
   Cloudflare Pages       Vultr VPS
```

---

## 3. Stack Propuesto

### Frontend
| Tecnología | Uso |
|------------|-----|
| JS Vanilla | UI minimalista |
| SASS | Estilos |
| i18n | Detección automática de idioma |

### Backend
| Tecnología | Uso |
|------------|-----|
| Python 3.14 | Runtime |
| FastAPI | API REST |
| PostgreSQL | BD principal |
| Redis | Cache + sesiones |
| Claude API | Análisis de prompts |

### Hosting
| Servicio | Uso |
|----------|-----|
| Cloudflare Pages | Frontend |
| Vultr VPS | Backend |
| Cloudflare R2 | Storage |

### Auth
| Servicio | Región |
|----------|--------|
| Google OAuth | Global |
| WeChat/Alipay | China |
| VK/Yandex | Rusia |
| Magic Link | Fallback |

---

## 4. Fases

### Fase 1: Solo Chuchu
- Un controlador
- Volumen limitado
- Validar modelo

### Fase 2: Red de Controladores
- Múltiples controladores
- Sistema de asignación
- Revenue share

### Fase 3: Escala
- 24/7 global
- Especialización
- QA cruzado

---

## 5. Cuando se Inicie

Seguir arquitectura de lawofone.cl:

1. **Frontend:**
   - Cloudflare Pages
   - `_headers` con CSP
   - CI/CD con GitHub Actions

2. **Backend:**
   - VPS con Docker
   - nginx reverse proxy
   - Rate limiting

3. **Seguridad:**
   - HTTPS obligatorio
   - CORS restringido
   - Input validation
   - OAuth seguro

---

## 6. Dominio

Opciones:
- human.ia (ccTLD India)
- humanpoint.ai
- we-human.ia

---

## 7. Estado Actual

- [x] Visión documentada
- [ ] Definir dominio
- [ ] Diseñar UI
- [ ] Implementar MVP
- [ ] Buscar beta testers

**Progreso: 5%** (solo idea)

---

*Documento generado: 4 Enero 2026*
