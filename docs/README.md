# Trust & Security Behavioral Lab (TSBL)

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Proyecto de Grado** — Cuantificación de la Resiliencia Cognitiva mediante Biometría Conductual Multimodal y Arquitecturas Predictivas V-JEPA 2 para la Prevención de Ingeniería Social en Fintech.

**Autores:** Camilo Yanten Santacruz, Nicolle Tatiana Quijano Jacome  
**Institución:** [Por confirmar]  
**Director de Tesis:** [Por asignar]

---

## Visión del Proyecto

TSBL es un framework de detección de **Vacilación Cognitiva** en tiempo real que integra:
- **Biometría facial** (MediaPipe Face Mesh, 468 landmarks, 30 fps)
- **Telemetría DOM** (interacciones mouse/teclado/scroll)
- **Embeddings predictivos** (V-JEPA 2 adaptado a landmarks)
- **Fricción de Seguridad Positiva** (4 niveles adaptativos)
- **Score de Resiliencia del Usuario** (SRU) con análisis longitudinal RLM

Todo opera en **Edge** (navegador del usuario) con privacidad por diseño: **nunca se transmiten imágenes faciales crudas**.

---

## Estado del Proyecto (Scrum)

| Sprint | Estado | Entregable Principal | Fecha Inicio | Fecha Fin |
|:---:|:---:|:---|:---:|:---:|
| Sprint 0 | 🟡 En progreso | Setup de infraestructura y arquitectura base | 2026-05-23 | 2026-05-30 |
| Sprint 1 | ⚪ Planificado | Pipeline de captura (MediaPipe + WebSocket) | 2026-05-31 | 2026-06-13 |
| Sprint 2 | ⚪ Planificado | Motor de embeddings (RDL + V-JEPA 2 adapter) | 2026-06-14 | 2026-06-27 |
| Sprint 3 | ⚪ Planificado | Detector VC + Calibración θ + FSP | 2026-06-28 | 2026-07-11 |
| Sprint 4 | ⚪ Planificado | SRU + RLM + Análisis estadístico | 2026-07-12 | 2026-07-25 |
| Sprint 5 | ⚪ Planificado | Integración E2E + Pruebas de carga + Documentación | 2026-07-26 | 2026-08-08 |

**Ver backlog completo:** [`docs/SCRUM_BACKLOG.md`](docs/SCRUM_BACKLOG.md)

---
## Quick Start

### Requisitos
- Python 3.11+
- Node.js 20+
- Git
- Cuenta Google Colab (para entrenamiento del Predictor JEPA Compacto)
- Webcam funcional (para pruebas locales)

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/[TU_USUARIO]/tsbl-project.git
cd tsbl-project

# 2. Ejecutar setup automático
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Iniciar entorno de desarrollo
./scripts/run_dev.sh
```

### Estructura del Proyecto

```
tsbl-project/
├── src/
│   ├── capture/          # Frontend: MediaPipe + DOM + WebSocket
│   ├── embedding/        # Backend: RDL + V-JEPA 2 + Predictor JC
│   ├── analysis/         # SRU + RLM post-sesión
│   ├── fsp/              # Motor de fricción de seguridad (CSS/JS)
│   └── api/              # FastAPI + WebSocket handler
├── tests/                # Unitarias, integración, fixtures
├── notebooks/            # Exploración y validación en Colab
├── configs/              # YAMLs de experimentos y CI
├── scripts/              # Automatización de setup y ejecución
├── docker/               # Contenedores para staging
└── docs/                 # Documentación técnica y de gestión
```

---

##  Demostración en Vivo

Para ver el sistema funcionando localmente:

```bash
# Terminal 1: Backend
python src/api/main.py

# Terminal 2: Frontend (servir archivos estáticos)
npx serve src/capture/ -p 8080

# Abrir en navegador: http://localhost:8080
# Permitir acceso a webcam cuando se solicite
```

---

## Métricas de Calidad

| Métrica | Umbral | Estado actual |
|:---|:---|:---:|
| Cobertura de tests unitarios | ≥ 80 % | 🟡 0 % |
| Latencia p95 end-to-end | < 200 ms | 🟡 N/A |
| Falsos positivos VC en baseline | < 5 % | 🟡 N/A |
| Poder estadístico (H1-H4) | ≥ 80 % | 🟢 Validado a priori |

---

##  Documentación

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Arquitectura de 3 capas y diagramas
- [`docs/SCRUM_BACKLOG.md`](docs/SCRUM_BACKLOG.md) — Backlog completo con historias de usuario
- [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) — Guía detallada de instalación por SO

---

##  Contribución

Este es un proyecto de grado académico. Las contribuciones externas están limitadas durante la fase de evaluación institucional. Contactar a los autores para colaboraciones post-grado.

---

## Licencia

MIT License — ver [LICENSE](LICENSE) para detalles.

> **Nota académica:** El código fuente, datasets anonimizados y modelos entrenados serán publicados con DOI al cierre del proyecto para garantizar reproducibilidad.
