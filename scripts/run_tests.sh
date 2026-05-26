#!/bin/bash
set -e

echo "🧪 TSBL — Suite de Tests Completa"
echo "=================================="
echo ""

source venv/bin/activate

# Tests unitarios Python
echo "📗 Tests unitarios Python..."
pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

# Tests unitarios JS
echo ""
echo "📘 Tests unitarios JavaScript..."
npm test -- --coverage

# Tests de integración
echo ""
echo "📙 Tests de integración..."
pytest tests/integration/ -v

# Mutation testing (opcional, lento)
if [ "$1" == "--mutation" ]; then
    echo ""
    echo "🔬 Mutation testing..."
    mutmut run --paths-to-mutate=src/
    mutmut results
fi

echo ""
echo "=================================="
echo "✅ Todos los tests pasaron!"
