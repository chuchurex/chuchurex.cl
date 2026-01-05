# CONTEXTO.md - Portafolio Chuchurex

## Quién soy

**Chuchurex (Chuchu)** - Desarrollador frontend chileno basado en Santiago. Stack principal: **SASS + JavaScript vanilla**. Trabajo con múltiples proyectos simultáneos usando AI como multiplicador de productividad (2.5-3x). Transparente sobre uso de IA con clientes.

---

## Infraestructura Base

```
Entorno local:     /Users/chuchurex/Sites/vigentes/
                   /Users/chuchurex/Sites/uchile/
Backend:           Python 3.14 + FastAPI + Docker
VPS:               Vultr Chile (64.176.12.233)
Frontend hosting:  Cloudflare Pages (deploy automático vía git push)
Herramientas:      VSCode + Claude Code + Claude Desktop + Antigravity
```

---

## Proyectos Activos

### 1. lawofone.cl (The One)
**Estado:** 75% completo | **Horas:** ~145h

Sitio editorial multiidioma (EN/ES/PT) del Material Ra. 16 capítulos filosóficos con glosario interactivo, sistema de referencias, y pipeline multimedia (PDF, audio TTS, videos YouTube).

```
Stack:        HTML5, SASS, JS vanilla, Node.js (build)
APIs:         Claude API (traducción), Fish Audio (TTS), YouTube API v3
Hosting:      Cloudflare Pages
Repo:         github.com/chuchurex/lawofone.cl
```

**Pendiente:** Traducir caps 8-16, generar multimedia completa, migrar feedback form a Workers.

---

### 2. chuchurex.cl (Astral / Cartas Natales)
**Estado:** 85% completo | **Horas:** ~80-100h

App de cartas natales astrológicas con biorritmos basados en Ra. Gráfico SVG, interpretaciones en español, sistema i18n propio (EN/ES/PT), accesibilidad WCAG AAA.

```
Stack:        HTML5, SASS, JS vanilla (~1400 líneas)
Backend:      Python + FastAPI + Kerykeion (Swiss Ephemeris)
Hosting:      Cloudflare Pages (front) + Vultr VPS Docker (API)
URLs:         chuchurex.cl | api.chuchurex.cl
```

**Pendiente:** Verificar biorritmos en prod, exportar PDF nativo, migrar a SSH keys.

---

### 3. entutinta.cl (E-commerce Prendas)
**Estado:** 65% - PAUSADO | **Horas:** ~9h

Rediseño de tienda WooCommerce de prendas personalizadas. Diseño completo desarrollado (CSS + PHP), pero aplicado erróneamente a producción. Restaurado y pivoteado a ambiente demo.

```
Stack:        WordPress + WooCommerce + Storefront Child Theme
Diseño:       CSS Variables, Mobile-first, WCAG 2.1
Demo:         entutinta.chuchurex.cl (por configurar)
```

**Bloqueadores:** phpMyAdmin caído (sesiones PHP), servidor compartido restrictivo.
**Próximo paso:** Migrar demo a subdominio personal.

---

### 4. elultimodisco.cl (Radio Web)
**Estado:** 95% completo | **Horas:** ~6h

Sitio para programa de radio. Grilla visual estilo NTS Radio con contenido de Instagram. WordPress child theme con diseño estático.

```
Stack:        HTML5, CSS Grid, JS vanilla, WordPress Child Theme
Hosting:      FTP manual (50.31.188.162)
Referencia:   nts.live
```

**Pendiente:** Solo activar tema desde wp-admin.

---

### 5. systema.cl (Rediseño Industrial)
**Estado:** 15% - Cotizado | **Horas:** ~1h (+ 3-5h desarrollo)

Rediseño web para empresa industrial chilena (torres de enfriamiento, hidrolavado). Cotización aprobada por $600.000 CLP.

```
Stack:        WordPress (tema existente del que soy autor)
Referencia:   termofrio-ingetrol.cl
```

**Próximo paso:** Obtener accesos, crear staging, implementar diseño.

---

### 6. Biblioteca Rudolf Steiner
**Estado:** 5% - Planificación | **Horas:** ~1-2h

Proyecto ambicioso para digitalizar la Gesamtausgabe (354+ volúmenes) en alemán, traducir a español, y distribuir en múltiples formatos.

```
Stack planeado: Python (scraping), PostgreSQL, DeepL/Claude API
Fuente:         bdn-steiner.ru
```

**Próximo paso:** Analizar estructura del sitio fuente, verificar aspectos legales.

---

### 7. Pipeline OCR (Ayurveda → Genérico)
**Estado:** 85% MVP | **Horas:** ~8-9h

Sistema de extracción OCR de PDFs/imágenes con limpieza de errores y generación de PDFs optimizados para móvil.

```
Stack:        Python, Tesseract OCR, poppler, ReportLab
Ubicación:    /Users/chuchurex/Sites/Antroposofia/ayurveda/
```

**Pendiente:** Detección automática de capítulos, preservar formato original.

---

## Dashboard de Proyectos (En Desarrollo)

Objetivo: Dashboard en **lc.xeruhcuhc.chuchurex.cl** para trackear automáticamente todos los proyectos.

```
Arquitectura:
- Carpetas locales con CONTEXTO.md por proyecto
- GitHub repos individuales con git hooks automáticos
- FastAPI backend + Cloudflare Pages frontend
- Actualización automática post-sesión de desarrollo
```

---

## Patrones de Trabajo

### Preferencias de Código
- **CSS:** SASS modular con variables, mobile-first
- **JS:** Vanilla, sin frameworks (excepto cuando cliente lo requiere)
- **Python:** FastAPI + Docker para backends
- **Documentación:** Markdown, archivos CONTEXTO.md por proyecto

### Flujo de Trabajo
1. Sesiones de 4h enfocadas
2. Q&A rápido para establecer requerimientos
3. Handoff via markdown entre herramientas AI
4. CONTEXTO.md actualizado al final de cada sesión

### Comunicación
- Prefiero español
- Conciso y organizado
- Step-by-step para tareas complejas
- Transparente sobre AI con clientes

---

## Tiempo Total Invertido (Estimado)

| Proyecto              | Horas         |
| --------------------- | ------------- |
| lawofone.cl           | ~145h         |
| chuchurex.cl (astral) | ~100h         |
| entutinta.cl          | ~9h           |
| elultimodisco.cl      | ~6h           |
| systema.cl            | ~1h           |
| Steiner Library       | ~2h           |
| OCR Pipeline          | ~9h           |
| **TOTAL**             | **~280-300h** |

---

## Próximas Prioridades

1. **entutinta.cl:** Configurar demo en subdominio personal
2. **lawofone.cl:** Completar traducciones caps 8-16
3. **systema.cl:** Obtener accesos e implementar
4. **Dashboard:** Configurar tracking automático de proyectos
5. **chuchurex.cl:** Verificar biorritmos en producción

---

## Visión a Futuro

**human.ia** - Plataforma global donde usuarios envían ideas de proyectos en su idioma nativo y reciben desarrollo asistido por AI de una red de "AI controllers". Evolución del concepto inicial de cotización chilena hacia desarrollo ilimitado global.

---

*Última actualización: 4 enero 2026*
*Generado para handoff a Claude Code*
