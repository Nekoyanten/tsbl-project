#!/bin/bash
set -e

ENV=${1:-backend}

case $ENV in
    backend)
        echo "🖥️  Iniciando backend (FastAPI + WebSocket)..."
        source venv/bin/activate
        uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    frontend)
        echo "🌐 Sirviendo frontend estático..."
        npx serve src/capture/ -p 8080 --cors
        ;;
    full)
        echo "🚀 Iniciando stack completo (requiere Docker)..."
        docker-compose -f docker/docker-compose.yml up --build
        ;;
    test)
        echo "🧪 Ejecutando suite de tests..."
        source venv/bin/activate
        pytest tests/ -v --tb=short
        ;;
    *)
        echo "Uso: ./scripts/run_dev.sh [backend|frontend|full|test]"
        exit 1
        ;;
esac
