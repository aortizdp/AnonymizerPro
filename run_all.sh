#!/bin/bash

# 1. Activar l'entorn virtual si existeix
if [ -d "venv" ]; then
    echo "🐍 Activant l'entorn virtual..."
    source venv/bin/activate
fi

echo "🚀 Engeguant AI Anonymizer Pro..."

# 2. Iniciar el Backend (FastAPI) en segon pla
echo "📡 Iniciant Backend al port 7000..."
uvicorn backend.main:app --host 0.0.0.0 --port 7000 &
BACKEND_PID=$!

# 3. Iniciar el Frontend (Streamlit)
echo "💻 Iniciant Frontend..."
streamlit run frontend/app.py

# 4. Quan es tanca Streamlit (Ctrl+C), matem també el procés del backend
echo "🛑 Aturant processos..."
kill $BACKEND_PID
