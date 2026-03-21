#!/usr/bin/env bash
# PromptShield — One-command setup and start

set -e
echo "========================================"
echo "  PromptShield — Setup & Launch"
echo "========================================"

ROOT="$(cd "$(dirname "$0")" && pwd)"

# Step 1: Train model
echo ""
echo "[1/3] Training injection detection model..."
cd "$ROOT"
pip install scikit-learn numpy --quiet
python training/generate_dataset.py
python training/train_model.py

# Step 2: Start backend
echo ""
echo "[2/3] Starting FastAPI backend on :8000..."
cd "$ROOT/backend"
pip install -r requirements.txt --quiet
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
sleep 2

# Step 3: Start frontend
echo ""
echo "[3/3] Starting Next.js frontend on :3000..."
cd "$ROOT/frontend"
npm install --silent
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  PromptShield is running!"
echo "  Frontend: http://localhost:3000"
echo "  API Docs: http://localhost:8000/docs"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" INT TERM
wait
