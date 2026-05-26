# TSBL — Backlog de Producto (Scrum)

> **Metodología:** Scrum adaptado para proyecto de grado  
> **Duración de Sprints:** 2 semanas  
> **Rol del Product Owner:** Director de tesis + Autores (Camilo & Nicolle)  
> **Rol del Scrum Master:** Camilo Yanten Santacruz  
> **Equipo de Desarrollo:** Camilo Yanten Santacruz, Nicolle Tatiana Quijano Jacome  
> **Asesor Técnico:** [Asistente IA — rol consultivo en arquitectura y revisión de código]

---

## Visión del Producto

> "Para los usuarios de plataformas Fintech en Colombia que enfrentan riesgo de fraude por ingeniería social, TSBL es un framework de biometría conductual que detecta la vacilación cognitiva en tiempo real y activa fricciones de seguridad adaptativas, a diferencia de las soluciones comerciales actuales que solo reaccionan al score de riesgo transaccional."

---

## Épicas y Historias de Usuario

### Épica 1: Captura Multimodal Privada (Capa 1)
**Objetivo:** Capturar landmarks faciales y telemetría DOM en el navegador del usuario sin comprometer privacidad.

| ID | Historia de Usuario | Criterios de Aceptación | Estimación (story points) | Sprint |
|:---:|:---|:---|:---:|:---:|
| US-1.1 | *Como* usuario de TSBL, *quiero* que el sistema acceda a mi webcam *para* capturar mi configuración facial inicial, *pero* nunca transmitir imágenes crudas al servidor. | 1. MediaPipe Face Mesh corre 100% en el navegador. 2. El payload WebSocket solo contiene arrays numéricos (468×3). 3. No hay blobs de imagen en la red (verificado con Wireshark). | 8 | Sprint 1 |
| US-1.2 | *Como* investigador, *quiero* capturar eventos DOM (clicks, scroll, tecleo) *para* correlacionar comportamiento de interacción con estado cognitivo. | 1. Todos los eventos de riesgo tienen timestamp ±5 ms. 2. Los inputs sensibles se hashean (SHA-256 truncado). 3. El schema JSON se valida contra `DOMTelemetryEvent.json`. | 5 | Sprint 1 |
| US-1.3 | *Como* usuario, *quiero* que mis datos de sesión se sincronicen correctamente *para* que el análisis sea preciso temporalmente. | 1. Jitter entre landmarks y DOM events < 50 ms. 2. Buffer de 1 segundo con retransmisión ante pérdida de paquetes. 3. Reconexión automática ante corte de WebSocket < 3 s. | 5 | Sprint 1 |
| US-1.4 | *Como* jurado evaluador, *quiero* ver una demostración visual del sistema funcionando *para* validar la viabilidad técnica. | 1. Página HTML de demo muestra landmarks superpuestos en video en tiempo real. 2. Panel de debug muestra eventos DOM capturados. 3. Gráfico en vivo de δ(W) cuando el usuario reacciona a estímulos. | 5 | Sprint 1 |

**Definición de Done (Épica 1):**
- [ ] Cobertura de tests unitarios (Jest) ≥ 70%
- [ ] Demo funcional accesible en `http://localhost:8080`
- [ ] Validación de privacidad: 0 imágenes transmitidas (verificado con proxy)

---

### Épica 2: Motor de Embeddings Predictivos (Capa 2)
**Objetivo:** Adaptar V-JEPA 2 para procesar landmarks faciales y detectar divergencias conductuales.

| ID | Historia de Usuario | Criterios de Aceptación | SP | Sprint |
|:---:|:---|:---|:---:|:---:|
| US-2.1 | *Como* desarrollador, *quiero* convertir secuencias de landmarks en tensores de video *para* alimentar el X-Encoder de V-JEPA 2. | 1. RDL genera tensores (3, 16, 256, 256) determinísticos. 2. Movimiento de un landmark altera el tensor resultante (test de preservación topológica). 3. Procesamiento de 1 segundo de video < 50 ms en CPU. | 8 | Sprint 2 |
| US-2.2 | *Como* científico de datos, *quiero* utilizar el X-Encoder de V-JEPA 2 con pesos congelados *para* extraer embeddings de 1024 dimensiones. | 1. Inferencia en Google Colab T4 < 200 ms por ventana de 8 s. 2. Embeddings reproducibles (misma entrada → mismo vector, ±1e-5). 3. Sin fine-tuning requerido para fase de prototipo. | 8 | Sprint 2 |
| US-2.3 | *Como* arquitecto de ML, *quiero* entrenar un Predictor JEPA Compacto *para* predecir embeddings futuros y detectar anomalías. | 1. PJC tiene 38M parámetros entrenables (verificable con `torchsummary`). 2. Entrenamiento en Colab T4 completa en < 4 horas con dataset de 100 sesiones. 3. MSE en validación LOSO < 0.15. | 13 | Sprint 2 |
| US-2.4 | *Como* investigador, *quiero* calcular la divergencia coseno entre predicción y baseline *para* cuantificar la vacilación cognitiva. | 1. δ(W) ∈ [0, 2] para todas las entradas. 2. δ = 0 para identidad perfecta, δ = 1 para ortogonalidad, δ = 2 para anticorrelación. 3. Lanzamiento de ValueError ante vector nulo. | 3 | Sprint 2 |
| US-2.5 | *Como* jurado, *quiero* ver un notebook de Colab ejecutable *para* validar la arquitectura de embeddings sin instalar nada localmente. | 1. Notebook `02_vjepa_landmark_adapter.ipynb` ejecutable en Colab. 2. Celda de demo que muestra δ(W) para landmarks sintéticos (neutral vs. estresado). 3. Gráficos de embeddings PCA/t-SNE comparando baseline vs. estímulo. | 5 | Sprint 2 |

**Definición de Done (Épica 2):**
- [ ] Notebook de Colab ejecutable con demo visual
- [ ] Tests unitarios (pytest) con cobertura ≥ 80%
- [ ] Métrica de latencia validada: p95 < 200 ms

---

### Épica 3: Detección de VC y Fricción de Seguridad (Capa 2-4)
**Objetivo:** Detectar episodios de vacilación cognitiva y activar intervenciones adaptativas.

| ID | Historia de Usuario | Criterios de Aceptación | SP | Sprint |
|:---:|:---|:---|:---:|:---:|
| US-3.1 | *Como* sistema, *quiero* calibrar un umbral individual θ por usuario *para* personalizar la detección de VC. | 1. θ_i = percentil 95 de δ(W) en baseline de 30 s. 2. Descarte de primeros 5 s (warm-up). 3. Validación LOSO: sensibilidad ≥ 75%, especificidad ≥ 80%. | 8 | Sprint 3 |
| US-3.2 | *Como* sistema, *quiero* detectar episodios de VC de al menos 1.6 s *para* filtrar picos espurios. | 1. Episodio requiere ≥ 2 ventanas consecutivas con δ > θ. 2. Duración mínima 1.6 s (2 ventanas × 0.8 s de stride). 3. No más de 5% de falsos positivos en sesiones neutrales. | 5 | Sprint 3 |
| US-3.3 | *Como* usuario, *quiero* recibir una pausa micro de 800 ms cuando el sistema detecta vacilación leve *para* reconsiderar mi acción sin interrupción visible. | 1. Nivel 1 FSP activa setTimeout de 800 ms antes del handler del evento. 2. Invisible al usuario (no hay cambio visual). 3. Latencia añadida < 5 ms (scheduling). | 3 | Sprint 3 |
| US-3.4 | *Como* usuario, *quiero* que elementos de riesgo se resalten en naranja cuando la vacilación es moderada *para* que preste atención antes de interactuar. | 1. Nivel 2 FSP inyecta CSS con outline y animación pulse. 2. Solo afecta elementos marcados isRiskElement = true. 3. Renderizado < 16 ms (1 frame). | 3 | Sprint 3 |
| US-3.5 | *Como* usuario, *quiero* ver un aviso no bloqueante cuando la vacilación es alta *para* tener 4 segundos de reflexión antes de continuar. | 1. Nivel 3 FSP muestra toast semántico con role="alert". 2. Contador regresivo de 4 s. 3. Usuario puede descartar o continuar (no es bloqueo). | 3 | Sprint 3 |
| US-3.6 | *Como* usuario en riesgo severo, *quiero* que el sistema bloquee temporalmente la acción *para* que escriba una confirmación consciente antes de proceder. | 1. Nivel 4 FSP desactiva el elemento (disabled=true). 2. Modal con campo de texto obligatorio: "Confirmo que conozco al beneficiario". 3. Desbloqueo solo tras texto exacto ingresado. | 5 | Sprint 3 |
| US-3.7 | *Como* jurado, *quiero* ver una demo interactiva donde pueda "experimentar" los 4 niveles de FSP *para* evaluar la experiencia de usuario. | 1. Página de demo con 4 botones que simulan cada nivel de FSP. 2. Visualización en tiempo real de δ(W) y nivel activo. 3. Registro de interacción en log visible. | 5 | Sprint 3 |

**Definición de Done (Épica 3):**
- [ ] Demo interactiva de 4 niveles de FSP accesible en navegador
- [ ] Tasa de falsos positivos < 5% en piloto (n = 16)
- [ ] Validación de accesibilidad: FSP cumple WCAG 2.1 AA

---

### Épica 4: Score de Resiliencia y Análisis Longitudinal (Capa 3)
**Objetivo:** Construir el SRU con interpretabilidad y análisis recursivo de sesiones.

| ID | Historia de Usuario | Criterios de Aceptación | SP | Sprint |
|:---:|:---|:---|:---:|:---:|
| US-4.1 | *Como* científico de datos, *quiero* entrenar un modelo de regresión logística regularizada *para* predecir comportamiento de riesgo a partir de features conductuales. | 1. Features: N_VC, T_VC, δ_max, ROT, contexto (todas transformadas y documentadas). 2. Regularización L2 (λ = 1.0). 3. AUC-ROC en validación > 0.80. | 8 | Sprint 4 |
| US-4.2 | *Como* regulador/auditor, *quiero* entender qué feature contribuyó a una predicción de riesgo específica *para* cumplir con GDPR Art. 22. | 1. SHAP values computados para cada predicción de SRU. 2. Gráfico de waterfall SHAP explicando contribución de cada variable. 3. Exportable a JSON para auditoría. | 5 | Sprint 4 |
| US-4.3 | *Como* investigador, *quiero* que el análisis RLM procese sesiones largas en subventanas de 5 minutos *para* detectar patrones de vulnerabilidad no visibles en ventanas cortas. | 1. Segmentación automática en subventanas de 5 minutos. 2. Prompt estructurado por subventana. 3. Salida P_RLM ∈ [0,1] que modula SRU base en ±15 puntos. | 8 | Sprint 4 |
| US-4.4 | *Como* jurado, *quiero* ver un dashboard con el SRU de usuarios de demo *para* evaluar la utilidad del indicador. | 1. Panel web que muestra lista de sesiones con SRU final. 2. Filtros por rango de SRU, número de VC, duración de sesión. 3. Exportación a CSV para análisis externo. | 5 | Sprint 4 |

**Definición de Done (Épica 4):**
- [ ] Dashboard de SRU funcional con datos de demo
- [ ] Interpretabilidad SHAP verificable por feature
- [ ] Precisión del SRU: AUC > 0.80 en validación

---

### Épica 5: Validación Experimental y Documentación
**Objetivo:** Ejecutar el experimento controlado y documentar resultados para evaluación de jurados.

| ID | Historia de Usuario | Criterios de Aceptación | SP | Sprint |
|:---:|:---|:---|:---:|:---:|
| US-5.1 | *Como* investigador, *quiero* reclutar 128 participantes estratificados *para* validar estadísticamente las 4 hipótesis. | 1. Estratificación por edad y nivel socioeconómico. 2. Cuota mínima n=8 por celda. 3. Consentimiento informado de dos etapas aprobado por CEISH. | 8 | Sprint 5 |
| US-5.2 | *Como* investigador, *quiero* implementar 5 escenarios de phishing simulado de alta sofisticación *para* inducir vacilación cognitiva realista. | 1. Escenarios basados en casos reales reportados por Superintendencia Financiera. 2. Validación de expertos: 3 profesionales califican realismo > 5.5/7. 3. Aleatorización de orden mediante cuadrado latino. | 8 | Sprint 5 |
| US-5.3 | *Como* investigador, *quiero* ejecutar análisis estadístico con corrección de Holm-Bonferroni *para* controlar error tipo I en 4 hipótesis. | 1. Reporte de p brutos y ajustados. 2. Tamaños de efecto (Cohen's d, AUC, RR) con IC 95%. 3. Análisis de sensibilidad (3 escenarios alternativos). | 5 | Sprint 5 |
| US-5.4 | *Como* estudiante de grado, *quiero* generar el documento final de tesis con índice de similitud < 15% *para* cumplir con normativa institucional. | 1. Turnitin < 15%. 2. Secciones completas según plantilla institucional. 3. Referencias en formato Vancouver o APA consistente. | 8 | Sprint 5 |
| US-5.5 | *Como* investigador, *quiero* publicar el dataset anonimizado y el código fuente con DOI *para* garantizar reproducibilidad. | 1. Dataset en Zenodo/figshare con licencia CC-BY-NC. 2. Código en GitHub con instrucciones de reproducción validadas en máquina limpia. 3. Pre-registro del protocolo en OSF. | 5 | Sprint 5 |

**Definición de Done (Épica 5):**
- [ ] Tesis/documento de grado aprobado por director
- [ ] Dataset y código publicados con DOI
- [ ] Presentación de 15 min lista para jurados

---

## Métricas de Velocidad (Velocity)

| Sprint | Story Points Planificados | Story Points Completados | Velocity |
|:---:|:---:|:---:|:---:|
| Sprint 0 | 21 | 🔄 En progreso | — |
| Sprint 1 | 23 | — | — |
| Sprint 2 | 29 | — | — |
| Sprint 3 | 32 | — | — |
| Sprint 4 | 26 | — | — |
| Sprint 5 | 34 | — | — |
| **Total** | **165** | — | — |

---

## Sprint Actual: Sprint 0 — "Cimientos" (23 Mayo – 30 Mayo 2026)

**Objetivo del Sprint:** Establecer infraestructura de desarrollo, arquitectura base y primeros entregables visibles para demostración a directores.

### Historias comprometidas:
- [ ] **US-0.1:** Crear repositorio GitHub con estructura profesional y CI/CD básico (5 SP)
- [ ] **US-0.2:** Generar scripts de setup automático (setup.sh, run_dev.sh) (3 SP)
- [ ] **US-0.3:** Documentar arquitectura en ARCHITECTURE.md con diagramas (5 SP)
- [ ] **US-0.4:** Crear notebook base de Colab para validación de concepto (5 SP)
- [ ] **US-0.5:** Implementar servidor WebSocket básico (FastAPI) + cliente HTML de prueba (3 SP)

### Daily Standup (formato asíncrono en GitHub Issues):
Cada día, cada miembro responde en el issue del sprint:
1. ¿Qué hice ayer?
2. ¿Qué haré hoy?
3. ¿Qué bloqueos tengo?

### Sprint Review (30 Mayo):
Demostración a director de tesis de:
- Repo GitHub funcional con CI verde
- Servidor WebSocket ejecutándose localmente
- Página HTML que muestra "Hello TSBL" y se conecta por WebSocket

### Sprint Retrospective (30 Mayo):
- ¿Qué funcionó bien?
- ¿Qué mejorar?
- ¿Qué compromisos tomamos para Sprint 1?

---

## 🔧 Herramientas de Gestión Recomendadas

| Propósito | Herramienta | Enlace/Config |
|:---|:---|:---|
| **Repositorio de código** | GitHub | `https://github.com/[TU_USUARIO]/tsbl-project` |
| **Project Board (Kanban)** | GitHub Projects | Tablero con columnas: Backlog, To Do, In Progress, Review, Done |
| **Issues / Historias** | GitHub Issues | Cada US es un issue con labels: `epic-1`, `sprint-1`, `priority-high` |
| **Documentación colaborativa** | Notion / Google Docs | Para notas de reuniones con director |
| **Notebooks ejecutables** | Google Colab | `notebooks/` sincronizados con GitHub |
| **Comunicación async** | GitHub Discussions | Para decisiones técnicas documentadas |

---

## Plantilla para Nuevas Historias de Usuario

```markdown
## US-X.Y: [Título descriptivo]

**Como** [rol],  
**quiero** [acción],  
**para** [beneficio/valor].

### Criterios de Aceptación
1. [Criterio medible y verificable]
2. [Criterio medible y verificable]
3. [Criterio medible y verificable]

### Notas Técnicas
- [Dependencias, librerías, consideraciones de arquitectura]

### Estimación: [X] story points
### Sprint: [Sprint Z]
```

---

*Última actualización: 2026-05-23*  
*Próxima revisión: Fin de Sprint 0 (2026-05-30)*
