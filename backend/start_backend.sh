#!/bin/bash
# Startup script for ANTIGRAVITY Python/FastAPI Backend

echo "Starting ANTIGRAVITY Backend..."
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Install dependencies if not already present
echo "Installing dependencies..."
pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt

# Run FastAPI app
echo "Launching FastAPI server..."
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
