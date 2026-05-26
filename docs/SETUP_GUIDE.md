# Guía de Instalación y Configuración de TSBL

> **Versión:** 1.0  
> **Fecha:** 2026-05-23  
> **Ambientes soportados:** Linux (Ubuntu 22.04+), macOS (13+), Windows 11 (WSL2 recomendado)

---

## Requisitos Previos

### Hardware mínimo para desarrollo
- CPU: 4 cores (8 threads recomendado)
- RAM: 8 GB (16 GB recomendado)
- Almacenamiento: 10 GB libres
- Webcam funcional (para pruebas de captura)
- Conexión a internet estable (para descarga de modelos y dependencias)

### Software requerido
| Herramienta | Versión mínima | Verificar instalación |
|:---|:---:|:---|
| Python | 3.11 | `python --version` |
| Node.js | 20.x | `node --version` |
| npm | 10.x | `npm --version` |
| Git | 2.40 | `git --version` |
| Docker | 24.x (opcional) | `docker --version` |

### Cuentas necesarias
- [ ] GitHub (para repositorio y CI/CD)
- [ ] Google Colab (para entrenamiento del Predictor JEPA Compacto)
- [ ] Opcional: cuenta ngrok (para exponer localhost temporalmente a jurados)

---

## Instalación Paso a Paso

### Paso 1: Clonar repositorio

```bash
git clone https://github.com/[TU_USUARIO]/tsbl-project.git
cd tsbl-project
```

### Paso 2: Ejecutar setup automático

El script `setup.sh` detecta tu sistema operativo e instala todo automáticamente:

```bash
# Linux / macOS
chmod +x scripts/setup.sh
./scripts/setup.sh

# Windows (PowerShell como Administrador, o WSL2)
# Recomendado: usar WSL2 para compatibilidad total
wsl ./scripts/setup.sh
```

**¿Qué hace `setup.sh`?**
1. Crea entorno virtual de Python (`venv/`) con dependencias de `requirements.txt`
2. Instala dependencias Node.js (`package.json`)
3. Descarga pesos preentrenados de V-JEPA 2 (si no existen)
4. Crea directorios de datos (`data/raw`, `data/processed`, `data/models`)
5. Verifica que MediaPipe se ejecuta correctamente en el navegador
6. Ejecuta tests de smoke para validar instalación

### Paso 3: Verificar instalación

```bash
# Test de Python
python -c "import torch; import mediapipe; print('✅ Python OK')"

# Test de Node.js
node -e "console.log('✅ Node OK')"

# Test de servidor (debe levantar sin errores)
python src/api/main.py --smoke-test
```

---

## Estructura de Entornos

```
tsbl-project/
├── venv/                    # Entorno Python (auto-generado)
├── node_modules/            # Dependencias Node (auto-generado)
├── data/
│   ├── raw/                 # Datos de sesiones capturadas (NO versionados)
│   ├── processed/           # Embeddings y features extraídas
│   └── models/              # Pesos del Predictor JEPA Compacto (.pth)
├── logs/                    # Logs de ejecución (rotación automática)
└── .env                     # Variables de entorno (NO versionado, ver .env.example)
```

### Archivos de configuración de entorno

Copia `.env.example` a `.env` y configura:

```bash
cp .env.example .env
```

Variables obligatorias:
```env
# Servidor
TSBL_HOST=0.0.0.0
TSBL_PORT=8000
TSBL_ENV=development  # development | staging | production

# WebSocket
WS_HEARTBEAT_INTERVAL=30
WS_MAX_MESSAGE_SIZE=1048576  # 1 MB

# Modelos
VJEPA_WEIGHTS_PATH=data/models/vjepa2_vitl16.pth
PREDICTOR_WEIGHTS_PATH=data/models/predictor_jc_8layer.pth

# Base de datos (SQLite para desarrollo)
DATABASE_URL=sqlite:///data/tsbl_dev.db

# RLM (API externa)
RLM_API_KEY=sk-...  # Solo para producción/análisis post-sesión
RLM_MODEL=gpt-4o-mini  # Modelo económico para RLM

# Seguridad
SECRET_KEY=generar_con: openssl rand -hex 32
HASH_SALT=generar_con: openssl rand -hex 16
```

---

## Comandos de Desarrollo

### Iniciar entorno completo

```bash
# Terminal 1: Backend API + WebSocket
./scripts/run_dev.sh backend

# Terminal 2: Frontend estático (sirve src/capture/)
npx serve src/capture/ -p 8080 --cors

# O usar el script unificado (si prefieres Docker)
./scripts/run_dev.sh full  # Levanta backend + frontend + base de datos
```

### Ejecutar tests

```bash
# Tests unitarios Python
pytest tests/unit/ -v --cov=src --cov-report=html

# Tests unitarios JavaScript
npm test

# Tests de integración (requiere backend levantado)
pytest tests/integration/ -v

# Tests de carga (requiere k6 instalado)
k6 run tests/load/test_100_users.js

# Todo junto (CI/CD local)
./scripts/run_tests.sh
```

### Notebooks en Google Colab

1. Abre [Google Colab](https://colab.research.google.com)
2. Selecciona "Archivo > Subir cuaderno" y elige `notebooks/02_vjepa_landmark_adapter.ipynb`
3. Cambia runtime a GPU: "Entorno de ejecución > Cambiar tipo de entorno de ejecución > T4 GPU"
4. Ejecuta celdas secuencialmente (botón ▶️ o `Ctrl+Enter`)

**Sincronización con GitHub:**
```bash
# Instalar jupyter-repo2docker (opcional)
pip install jupyter-repo2docker

# O simplemente: subir manualmente notebooks modificados a GitHub
git add notebooks/
git commit -m "feat: actualiza notebook de validación de embeddings"
git push origin main
```

---

## Solución de Problemas Comunes

### Problema: MediaPipe no detecta la webcam

**Síntoma:** `face_mesh_wrapper.js` lanza `CameraError` o muestra canvas negro.

**Solución:**
1. Verificar permisos de cámara en el navegador (ícono 🔒 en barra de dirección)
2. Probar en Chrome/Edge (WebRTC más estable que Firefox para MediaPipe)
3. Si usas WSL2: la webcam no es nativa, usar [usbipd](https://github.com/dorssel/usbipd-win) o probar en Windows nativo
4. Alternativa: usar video de prueba pregrabado (`tests/fixtures/test_video.mp4`)

### Problema: V-JEPA 2 no carga en Colab (OOM)

**Síntoma:** `RuntimeError: CUDA out of memory` al cargar el X-Encoder.

**Solución:**
1. Reducir batch size: en `src/embedding/vjepa_adapter.py`, cambiar `BATCH_SIZE = 1`
2. Usar CPU en Colab: cambiar runtime a "Ninguno" (más lento pero funciona)
3. Descargar pesos quantizados (si disponibles): contactar a asesor técnico

### Problema: WebSocket se desconecta cada 30 segundos

**Síntoma:** Cliente recibe `1006 Abnormal Closure`.

**Solución:**
1. Verificar que `WS_HEARTBEAT_INTERVAL` en `.env` está configurado
2. Si usas proxy inverso (nginx), aumentar `proxy_read_timeout`
3. En desarrollo: desactivar firewall temporalmente para verificar

### Problema: Tests de integración fallan por dependencias circulares

**Síntoma:** `ImportError` o `ModuleNotFoundError` en tests.

**Solución:**
```bash
# Reinstalar en modo editable
pip install -e .

# O verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

---

## Checklist de Verificación Post-Instalación

- [ ] `python src/api/main.py --smoke-test` devuelve `✅ OK`
- [ ] `npm test` ejecuta sin errores (0 tests por ahora es OK)
- [ ] Abrir `http://localhost:8080` muestra página de demo básica
- [ ] WebSocket se conecta sin errores en consola del navegador
- [ ] Colab notebook `01_exploracion_baseline.ipynb` ejecuta celda 1 sin errores
- [ ] GitHub Actions (si configurado) muestra ✅ verde en último commit

---

## Contacto y Soporte

- **Issues técnicos:** Crear issue en GitHub con label `question` o `bug`
- **Consultas metodológicas:** Documentar en GitHub Discussions
- **Reuniones con director:** Agendar vía email con agenda pre-definida

---

*Documento mantenido por: Camilo Yanten Santacruz, Nicolle Tatiana Quijano Jacome*  
*Última actualización: 2026-05-23*
