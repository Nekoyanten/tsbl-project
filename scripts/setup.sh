#!/bin/bash
set -e  # Detener ante cualquier error

echo "🚀 TSBL — Script de instalación automática"
echo "========================================="
echo ""

# Detectar OS
OS=$(uname -s)
if [[ "$OS" == "Linux" ]]; then
    DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
elif [[ "$OS" == "Darwin" ]]; then
    DISTRO="macOS"
else
    echo "⚠️  Sistema no soportado nativamente. Usar WSL2 en Windows."
    exit 1
fi

echo "📦 Sistema detectado: $OS ($DISTRO)"
echo ""

# Verificar dependencias mínimas
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ Error: $1 no está instalado. Instalar antes de continuar."
        exit 1
    fi
    echo "✅ $1 detectado: $($1 --version | head -n1)"
}

check_command python
check_command node
check_command npm
check_command git

# Crear entorno virtual Python
echo ""
echo "🐍 Creando entorno virtual de Python..."
if [ ! -d "venv" ]; then
    python -m venv venv
fi
source venv/bin/activate

# Instalar dependencias Python
echo "📥 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Instalar dependencias Node.js
echo ""
echo "📥 Instalando dependencias Node.js..."
npm install

# Crear estructura de datos
echo ""
echo "📁 Creando directorios de datos..."
mkdir -p data/{raw,processed,models}
mkdir -p logs

# Copiar archivo de entorno si no existe
if [ ! -f ".env" ]; then
    echo "⚙️  Creando .env desde template..."
    cp .env.example .env
    echo "   ⚠️  IMPORTANTE: Editar .env con valores seguros antes de producción"
fi

# Descargar pesos de V-JEPA 2 (placeholder — se completará en Sprint 2)
echo ""
echo "📦 Verificando pesos de modelos..."
if [ ! -f "data/models/vjepa2_vitl16.pth" ]; then
    echo "   ⚠️  Pesos de V-JEPA 2 no encontrados. Se descargarán en Sprint 2."
    echo "      Instrucciones: ver docs/SETUP_GUIDE.md sección 'Modelos Preentrenados'"
fi

# Smoke test
echo ""
echo "🧪 Ejecutando smoke tests..."
python -c "import torch; import numpy; import fastapi; print('✅ Dependencias Python OK')"
node -e "console.log('✅ Node.js OK')"

# Mensaje final
echo ""
echo "========================================="
echo "✅ Instalación completada exitosamente!"
echo ""
echo "Próximos pasos:"
echo "  1. Editar .env con configuración local"
echo "  2. Ejecutar: ./scripts/run_dev.sh backend"
echo "  3. Abrir en navegador: http://localhost:8080"
echo "  4. Ver guía completa: docs/SETUP_GUIDE.md"
echo ""
echo "Sprint actual: Sprint 0 — Cimientos"
echo "Duración: 23 Mayo - 30 Mayo 2026"
echo "========================================="
