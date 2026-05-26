# 🎯 Sprint 0 — Resumen Ejecutivo: "Cimientos"

> **Período:** 23 Mayo — 30 Mayo 2026  
> **Objetivo:** Establecer infraestructura de desarrollo, arquitectura base y primeros entregables visibles.

---

## ✅ Entregables Completados

| # | Entregable | Estado | Ubicación |
|:---:|:---|:---:|:---|
| 1 | Repositorio GitHub con estructura profesional | ✅ Listo | `tsbl-project/` (local, listo para push) |
| 2 | Scripts de setup automático (setup.sh, run_dev.sh, run_tests.sh) | ✅ Listo | `scripts/` |
| 3 | Documentación de arquitectura con diagramas Mermaid | ✅ Listo | `docs/ARCHITECTURE.md` |
| 4 | Notebook de Colab ejecutable (validación de concepto) | ✅ Listo | `notebooks/01_exploracion_baseline.ipynb` |
| 5 | Servidor WebSocket básico (FastAPI) + REST API | ✅ Listo | `src/api/main.py` |
| 6 | Página HTML de demo con conexión WebSocket | ✅ Listo | `src/capture/index.html` |
| 7 | Configuración CI/CD (GitHub Actions) | ✅ Listo | `.github/workflows/ci.yml` |
| 8 | Backlog Scrum completo con 5 sprints planificados | ✅ Listo | `docs/SCRUM_BACKLOG.md` |
| 9 | Guía de instalación detallada | ✅ Listo | `docs/SETUP_GUIDE.md` |
| 10 | Dependencias Python y Node.js versionadas | ✅ Listo | `requirements.txt`, `package.json` |

---

## 🚀 Cómo Demostrar Esto a tu Director de Tesis (HOY)

### Opción A: Demo Local (5 minutos)

```bash
# 1. Ir al directorio del proyecto
cd tsbl-project

# 2. Crear entorno virtual e instalar dependencias mínimas
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn websockets

# 3. Iniciar servidor
python src/api/main.py

# 4. En otra terminal, servir el frontend
npx serve src/capture/ -p 8080

# 5. Abrir navegador en http://localhost:8080
# 6. Presionar "Iniciar Sesión" → ver conexión WebSocket activa
```

### Opción B: Mostrar Notebook en Colab (3 minutos)

1. Abrir [Google Colab](https://colab.research.google.com)
2. Subir `notebooks/01_exploracion_baseline.ipynb`
3. Ejecutar celdas 1-4 (verificación de entorno + simulación de baseline)
4. Mostrar gráficos de distribución δ(W) al director

### Opción C: Mostrar Estructura del Repo (2 minutos)

```bash
cd tsbl-project
tree -L 2  # o ls -R
git log --oneline  # si ya hiciste commit inicial
```

---

## 📋 Checklist para Cierre de Sprint 0

- [ ] Subir repositorio a GitHub (crear repo, push inicial)
- [ ] Ejecutar servidor localmente y verificar demo funciona
- [ ] Ejecutar notebook en Colab y verificar gráficos se generan
- [ ] Agregar director de tesis como colaborador en GitHub
- [ ] Programar Sprint Review con director (30 Mayo)
- [ ] Preparar 3 slides de presentación (estado, demo, plan Sprint 1)

---

## 🎯 Plan Sprint 1: "Captura Viva" (31 Mayo — 13 Junio)

**Objetivo:** Integrar MediaPipe Face Mesh real, telemetría DOM funcional, y sincronización temporal robusta.

**Historias comprometidas:**
- US-1.1: MediaPipe Face Mesh local con 468 landmarks
- US-1.2: DOM Telemetry Wrapper con schema JSON validado
- US-1.3: Sincronización temporal landmarks-DOM < 50 ms
- US-1.4: Demo visual con landmarks superpuestos en video

**Demo esperada para jurados:** Página web donde se ve la cara del usuario con 468 puntos verdes superpuestos, moviéndose en tiempo real, y un panel lateral mostrando eventos DOM capturados.

---

## 📞 Próximos Pasos Inmediatos

1. **Hoy:** Subir a GitHub, probar demo local, tomar screenshot/video para evidencia
2. **Mañana:** Compartir enlace de repo con director de tesis
3. **Esta semana:** Resolver dudas del director, ajustar alcance si es necesario
4. **30 Mayo:** Sprint Review — demostrar todo funcionando

---

*Generado: 2026-05-23*  
*Próxima actualización: Fin Sprint 0 (30 Mayo)*
