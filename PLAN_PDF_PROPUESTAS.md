# Plan: Generación de Propuestas PDF desde el Chat

## Objetivo
Permitir que el chatbot genere automáticamente propuestas en PDF para clientes que desarrollan una idea durante la conversación.

## Caso de Uso Piloto
Cliente del delivery con show en vivo: conversó su idea paso a paso y recibió un PDF profesional con la propuesta tecnológica.

## Pasos de Implementación

### Fase 1: Preparación del Sistema
**Objetivo:** Tener la infraestructura básica para generar PDFs

1. **Instalar dependencias en el servidor**
   - [ ] Subir `package.json` al VPS
   - [ ] Instalar `puppeteer` y `markdown-it` en el servidor
   - [ ] Crear carpeta `/var/www/chuchurex-api/pdf-generator/`
   - [ ] Copiar `generate-pdf.js` al servidor

2. **Crear templates base**
   - [ ] Template genérico de propuesta (markdown)
   - [ ] Sistema de variables para personalizar
   - [ ] Estilos CSS validados (los que ya tenemos)

### Fase 2: Integración con el Chat
**Objetivo:** Detectar cuándo generar una propuesta

3. **Actualizar system prompt**
   - [ ] Agregar capacidad de detectar ideas completas
   - [ ] Enseñarle a estructurar la información en formato propuesta
   - [ ] Instrucción para preguntar si quieren recibir PDF

4. **Crear endpoint `/generate-proposal`**
   ```python
   POST /generate-proposal
   Body: {
     "chat_id": "20260106_011504",
     "client_name": "Cliente Delivery Show",
     "project_summary": "...",
     "key_points": [...],
     "tech_stack": [...]
   }
   ```
   - [ ] Lee conversación completa del chat_id
   - [ ] Genera markdown con template
   - [ ] Ejecuta Node.js para crear PDF
   - [ ] Retorna URL del PDF generado

### Fase 3: Flujo Automatizado
**Objetivo:** Que el chat ofrezca el PDF al final

5. **Lógica de detección**
   - [ ] Chat detecta cuando se desarrolló una idea completa
   - [ ] Pregunta: "¿Te gustaría que te prepare una propuesta en PDF?"
   - [ ] Si acepta → genera PDF
   - [ ] Responde con: "Tu propuesta está lista: [URL]"

6. **Almacenamiento de PDFs**
   - [ ] Crear `/var/www/chuchurex-api/proposals/`
   - [ ] Servir estáticamente via nginx
   - [ ] URL: `https://api.chuchurex.cl/proposals/YYYYMMDD_HHMMSS.pdf`

### Fase 4: Template Inteligente
**Objetivo:** PDF se genera automáticamente del chat

7. **Procesamiento de conversación**
   - [ ] Función que analiza el chat completo
   - [ ] Extrae: problema, solución, features, fases
   - [ ] Genera estructura markdown automática
   - [ ] Aplica template con variables

8. **Personalización del PDF**
   Variables que se rellenan automáticamente:
   - [ ] `{CLIENT_NAME}` - nombre del cliente
   - [ ] `{PROJECT_NAME}` - nombre del proyecto
   - [ ] `{DATE}` - fecha actual
   - [ ] `{SUMMARY}` - resumen del proyecto
   - [ ] `{FEATURES}` - lista de funcionalidades
   - [ ] `{PHASES}` - fases sugeridas
   - [ ] `{CONTACT}` - carlos@chuchurex.cl

### Fase 5: Mejoras de UX
**Objetivo:** Experiencia premium

9. **Notificación de generación**
   - [ ] Mientras genera: "Preparando tu propuesta..."
   - [ ] Indicador de progreso visual
   - [ ] Al completar: botón de descarga

10. **Email automático** (opcional)
    - [ ] Pedir email al cliente
    - [ ] Enviar PDF adjunto
    - [ ] Usar SendGrid/Resend

### Fase 6: Refinamiento
**Objetivo:** Calidad profesional

11. **Ajustes de estilo**
    - [x] Logo solo en primera página
    - [x] Sin colores (solo negro)
    - [x] Texto 14px
    - [x] Footer al final del doc
    - [x] Espaciado optimizado
    - [ ] Numeración de páginas

12. **Validación de contenido**
    - [ ] Revisar ortografía automática
    - [ ] Verificar que tenga todas las secciones
    - [ ] Mínimo de calidad de contenido

## Estructura de Archivos Final

```
/var/www/chuchurex-api/
├── app.py                      # API principal
├── chats/                      # Conversaciones
├── proposals/                  # PDFs generados (servidos por nginx)
├── pdf-generator/
│   ├── package.json
│   ├── node_modules/
│   ├── generate-pdf.js         # Script principal
│   ├── templates/
│   │   └── proposal.md         # Template base
│   └── styles/
│       └── pdf-styles.css      # Estilos validados
└── utils/
    └── chat_analyzer.py        # Analiza chats para extraer info
```

## Ejemplo de Flujo Completo

```
Usuario: "Quiero hacer delivery de paellas con show en vivo"
Bot: [hace preguntas, desarrolla la idea]
Usuario: "Sí, me gusta"
Bot: "¿Te gustaría que te prepare una propuesta detallada en PDF?"
Usuario: "Sí"
Bot: "Preparando tu propuesta... ✓"
     "Tu propuesta está lista: https://api.chuchurex.cl/proposals/20260106_123456.pdf"
```

## Métricas de Éxito

- [ ] Tiempo de generación < 10 segundos
- [ ] PDFs profesionales y legibles
- [ ] 0 errores de formato
- [ ] Cliente satisfecho con el resultado

## Próximos Pasos Inmediatos

1. Mover `generate-pdf.js` y dependencias al servidor
2. Crear endpoint `/generate-proposal` básico
3. Probar generación manual con el chat del delivery
4. Iterar hasta tener calidad production

## Notas Importantes

- **Privacidad**: PDFs se generan con ID único, no indexables
- **Limpieza**: Borrar PDFs > 7 días automáticamente
- **Limitación**: Máximo 1 PDF por conversación
- **Fallback**: Si falla generación, ofrecer resumen por email

---

**Estado:** Piloto exitoso con cliente Delivery Show
**Próximo paso:** Implementar Fase 1
