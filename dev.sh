#!/bin/bash
# CHUCHUREX - Development Script
# Levanta frontend y backend en paralelo

FRONTEND_PORT=3010
BACKEND_PORT=8002

echo "Starting Chuchurex development servers..."

# Kill existing processes on ports
pkill -f "http.server $FRONTEND_PORT" 2>/dev/null
pkill -f "uvicorn.*$BACKEND_PORT" 2>/dev/null
lsof -ti:$FRONTEND_PORT | xargs kill -9 2>/dev/null
lsof -ti:$BACKEND_PORT | xargs kill -9 2>/dev/null
sleep 1

# Start backend
echo "Starting backend on port $BACKEND_PORT..."
cd backend
source .venv/bin/activate 2>/dev/null || python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -q
uvicorn app:app --host 127.0.0.1 --port $BACKEND_PORT &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 2

# Start frontend
echo "Starting frontend on port $FRONTEND_PORT..."
cd frontend
python3 -m http.server $FRONTEND_PORT --bind 127.0.0.1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "Servers running:"
echo "   Frontend: http://127.0.0.1:$FRONTEND_PORT"
echo "   Backend:  http://127.0.0.1:$BACKEND_PORT"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Servers stopped'; exit" INT
wait
