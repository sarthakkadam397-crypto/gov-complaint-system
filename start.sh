#!/usr/bin/env bash
cd "$(dirname "$0")"

echo "======================================================================"
echo "  NATIONAL GOVERNMENT COMPLAINT MANAGEMENT SYSTEM"
echo "  All-in-One Digital Public Grievance Redressal Platform"
echo "======================================================================"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is not installed or not in PATH!"
    exit 1
fi

if [ ! -f "complaints.db" ]; then
    echo "[INFO] First time initialization: Seeding database..."
    python3 seed_data.py
fi

echo "[STARTING] Launching server at http://127.0.0.1:5000/ ..."
python3 app.py
