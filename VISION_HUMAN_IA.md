# human.ia - Visión del Proyecto

## La Idea Central

**Una máquina global de proyectos IA.**

No es un servicio chileno. No es una agencia. Es una plataforma donde cualquier persona en el mundo escribe su idea y obtiene un proyecto desarrollado por humanos potenciados con IA.

---

## Concepto

### La Experiencia del Usuario

1. **Llega al sitio** → El navegador detecta idioma automáticamente
2. **Ve solo una caja** → Minimalismo absoluto. Un prompt. Nada más.
3. **Se loguea** → Google para occidente, alternativas para China/Rusia/etc.
4. **Escribe su idea** → En su idioma nativo
5. **Datos básicos** → Solo lo esencial para cotizar
6. **Recibe propuesta** → Precio, tiempo, fecha de entrega
7. **Acepta** → El proyecto entra a la cola
8. **Recibe su proyecto** → Desarrollado por un "controlador de IA"

---

## Arquitectura Humana

### Fase 1: Solo Chuchu
- Tú eres el único "controlador de IA"
- Todos los proyectos pasan por ti
- Capacidad: X proyectos/semana

### Fase 2: Red de Controladores
- Otros desarrolladores se unen como controladores
- Cada uno tiene su especialidad
- Sistema de asignación según skills
- Revenue share o fee por proyecto

### Fase 3: Escala
- Controladores en múltiples zonas horarias
- Proyectos 24/7
- Especialización por tipo de proyecto
- Quality assurance cruzado

---

## El Nombre

**human.ia**

- Juego de palabras: human + IA
- Dominio potencial: human.ia (ccTLD de India, disponibilidad por verificar)
- Alternativas: humanpoint.ai, humandot.ia, we-human.ia

---

## Stack Técnico (Borrador)

### Frontend
- JS Vanilla (tu expertise)
- SASS
- i18n automático por navegador
- UI minimalista: solo la caja del prompt

### Backend
- Python 3.14 + FastAPI
- Docker en VPS (Vultr u otro)

### Auth
- Google OAuth (principal)
- WeChat / Alipay (China)
- VK / Yandex (Rusia)
- Email magic link (fallback universal)

### Base de Datos
- PostgreSQL (proyectos, usuarios, cola)
- Redis (sesiones, cache)

### Procesamiento de Prompts
- Claude API para análisis y categorización
- Extracción automática de:
  - Tipo de proyecto
  - Complejidad estimada
  - Stack sugerido
  - Horas estimadas

### Sistema de Cola
- Dashboard de controladores
- Asignación por especialidad
- Tracking de progreso
- Comunicación con cliente

---

## Modelo de Negocio

### Pricing
- Basado en el análisis del prompt
- Fórmula: `(Horas_base × Complejidad × Valor_hora) / Multiplicador_IA`
- Precios en USD (moneda global)
- Conversión automática a moneda local

### Revenue (Fase 2+)
- Plataforma toma X% del proyecto
- Controlador recibe Y%
- Escala según volumen

---

## Diferenciadores

1. **Global desde el día 1** - No es "agencia chilena que vende afuera"
2. **Prompt-first** - La experiencia más simple posible
3. **Humanos + IA** - No es solo IA generando basura, hay craft humano
4. **Transparente** - El cliente sabe que usamos IA (caso Systema demostró que funciona)
5. **Red de controladores** - Escalable sin perder calidad

---

## Preguntas Abiertas

- [ ] ¿Dominio? human.ia vs alternativas
- [ ] ¿Idiomas iniciales? EN + ES + PT + ZH?
- [ ] ¿Cómo verificar controladores?
- [ ] ¿Cómo manejar disputas/refunds?
- [ ] ¿Escrow o pago directo?
- [ ] ¿Qué pasa con proyectos que fallan?

---

## Competencia Potencial

- Fiverr / Upwork (marketplaces genéricos)
- Agencies tradicionales
- No-code tools (Webflow, Bubble)
- AI-only generators (que producen basura)

**Diferencia:** Nosotros combinamos la velocidad de IA con el criterio humano.

---

## Primera Acción

Mover carta astral a `astral.chuchurex.cl` y usar `chuchurex.cl` como MVP de human.ia (o conseguir el dominio definitivo).

---

*Idea capturada: 1 de enero de 2026*
*Origen: Conversación sobre plataforma de cotización que evolucionó a visión global*
