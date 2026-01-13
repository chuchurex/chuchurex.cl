#!/bin/bash
# =============================================================================
# CHUCHUREX - Script de Desarrollo
# Inicia el backend y frontend para desarrollo local
# =============================================================================

echo "🚀 Iniciando Chuchurex Development Environment..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app_unified.py" ]; then
    echo "❌ Error: Ejecuta este script desde la raíz del proyecto uman.ia"
    exit 1
fi

# Verificar dependencias de Node
if [ ! -d "pdf-generator/node_modules" ]; then
    echo "📦 Instalando dependencias de PDF Generator..."
    cd pdf-generator && npm install && cd ..
fi

# Verificar entorno virtual Python
if [ ! -d ".venv" ] && [ ! -d "backend/.venv" ]; then
    echo "📦 Creando entorno virtual Python..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install fastapi uvicorn anthropic python-dotenv
else
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        source backend/.venv/bin/activate
    fi
fi

echo ""
echo "═══════════════════════════════════════════════"
echo "  🔧 Backend:  http://127.0.0.1:8002"
echo "  🌐 Frontend: http://127.0.0.1:3007"
echo "  📊 Chats:    http://127.0.0.1:8002/chats?key=chuchu2026"
echo "═══════════════════════════════════════════════"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Iniciar Backend
echo "🐍 Iniciando Backend (FastAPI)..."
uvicorn app_unified:app --reload --port 8002 &
BACKEND_PID=$!

# Esperar a que el backend inicie
sleep 2

# Iniciar Frontend
echo "🌐 Iniciando Frontend (Live Server)..."
cd frontend && npx live-server --port=3007 --no-browser &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Servicios iniciados. Presiona Ctrl+C para detener."
echo ""

# Mantener el script corriendo
wait
