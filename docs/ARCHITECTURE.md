# TSBL — Documento de Arquitectura

> **Versión:** 1.0 (Sprint 0)  
> **Fecha:** 2026-05-23  
> **Autores:** Camilo Yanten Santacruz, Nicolle Tatiana Quijano Jacome

---

## 1. Vista General de Arquitectura (C4 — Nivel 1: Contexto)

```mermaid
graph TB
    subgraph Usuario[" Usuario Fintech"]
        U[Cliente Web con Webcam]
    end

    subgraph TSBL[" TSBL Framework"]
        C[Capa 1: Captura Multimodal]
        E[Capa 2: Embeddings Predictivos]
        A[Capa 3: Análisis Longitudinal]
        F[Capa 4: Fricción de Seguridad]
    end

    subgraph Infraestructura["☁️ Infraestructura"]
        COL[Google Colab T4<br/>Entrenamiento ML]
        DB[(SQLite/PostgreSQL<br/>Datos de sesión)]
        RLM_API[API Externa RLM<br/>OpenAI/Anthropic]
    end

    U -->|Landmarks + DOM events| C
    C -->|Stream WebSocket| E
    E -->|δ(W), episodios VC| F
    E -->|Embeddings + features| A
    A -->|SRU final| DB
    A -.->|Análisis recursivo| RLM_API
    COL -.->|Pesos entrenados| E
```

---

## 2. Diagrama de Componentes (C4 — Nivel 3)

### 2.1. Capa 1 — Captura Multimodal

```mermaid
graph LR
    subgraph Browser[" Navegador del Usuario"]
        MP[MediaPipe Face Mesh<br/>468 landmarks, 30fps]
        DOM[DOM Telemetry Wrapper<br/>Eventos JS ±5ms]
        WS_CLIENT[WebSocket Client<br/>Buffer 1s, MessagePack]
        FSP_CSS[FSP Engine<br/>CSS/JS inyección]
    end

    subgraph Server[" Servidor FastAPI"]
        WS_SERVER[WebSocket Handler<br/>Jitter buffer 100ms]
        SESSION[Session Manager<br/>UUID v4, estado en memoria]
    end

    MP -->|Landmarks 468×3| WS_CLIENT
    DOM -->|JSON Schema| WS_CLIENT
    WS_CLIENT -->|wss://| WS_SERVER
    WS_SERVER -->|Ordenar/validar| SESSION
    FSP_CSS -->|Niveles 1-4| DOM
```

### 2.2. Capa 2 — Motor de Embeddings

```mermaid
graph LR
    subgraph Preprocessing["Preprocesamiento"]
        RDL[RDL Renderer<br/>Landmarks → (3,16,256,256)]
    end

    subgraph ML["Pipeline ML"]
        XENC[X-Encoder V-JEPA 2<br/>ViT-L/16, pesos congelados<br/>Salida: 1024-dim]
        PJC[Predictor JEPA Compacto<br/>8 capas, 38M params<br/>Salida: 1024-dim]
        DIV[Divergencia δ(W)<br/>1 - cosine_similarity]
        VC[Detector VC<br/>θ calibrado, ≥2 ventanas]
    end

    RDL -->|Tensores video| XENC
    XENC -->|Embeddings contextuales| PJC
    PJC -->|Ŝ_y predicho| DIV
    XENC -->|S_y observado| DIV
    DIV -->|δ(W)| VC
```

### 2.3. Capa 3 — Análisis y SRU

```mermaid
graph TB
    subgraph Features["Features de Sesión"]
        NVC[N_VC: número episodios]
        TVC[T_VC: duración promedio]
        DMAX[δ_max: mayor divergencia]
        ROT[ROT: ratio revisión riesgo]
        CTX[C_ctx: contexto ordinal]
    end

    subgraph Modelo["🤖 Modelo SRU"]
        LR[Regresión Logística<br/>L2 regularizada]
        SHAP[SHAP Values<br/>Interpretabilidad]
    end

    subgraph PostHoc["🔮 Análisis Longitudinal"]
        SEG[Segmentación 5min]
        RLM[RLM Processor<br/>Prompts recursivos]
        PRLM[P_RLM ∈ [0,1]]
    end

    NVC & TVC & DMAX & ROT & CTX --> LR
    LR -->|f(x)| SRU[SRU = 100×(1-f(x))]
    SEG -->|Resúmenes| RLM
    RLM --> PRLM
    PRLM -->|±15 puntos| SRU
    SRU --> SHAP
```

---

## 3. Diagrama de Secuencia — Detección de VC y Activación FSP

```mermaid
sequenceDiagram
    participant U as Usuario
    participant B as Browser (MediaPipe)
    participant WS as WebSocket
    participant API as FastAPI Server
    participant E as Embedding Engine
    participant F as FSP Engine

    Note over U,F: Fase 1: Baseline (30s)
    U->>B: Interacción neutral
    B->>WS: Landmarks + DOM (1Hz)
    WS->>API: Buffer validado
    API->>E: Construir B_usuario
    E-->>API: θ_i = P95(δ baseline)
    API-->>U: Baseline listo

    Note over U,F: Fase 2: Estímulo de phishing
    U->>B: Reacción a estímulo
    B->>WS: Landmarks (mayor variabilidad)
    WS->>API: Stream continuo
    API->>E: Calcular δ(W)

    alt δ(W) > θ_i (2+ ventanas)
        E-->>API: VC detectado
        API->>F: Activar FSP nivel proporcional
        F-->>U: Pausa/resaltado/aviso/bloqueo
    else δ(W) ≤ θ_i
        E-->>API: Comportamiento normal
    end

    Note over U,F: Fase 3: Post-sesión
    API->>E: Agregar features (N_VC, T_VC, etc.)
    E->>E: Calcular SRU base
    E->>RLM: Procesar subventanas 5min
    RLM-->>E: P_RLM
    E-->>API: SRU_final
    API-->>U: Reporte de sesión
```

---

## 4. Decisiones de Arquitectura (ADRs)

### ADR-001: MediaPipe en el Edge (no servidor)
**Estado:** Aceptado  
**Contexto:** GDPR Art. 9 categoriza biometría como dato especial. Transmisión de imágenes faciales crudas violaría principio de minimización.  
**Decisión:** MediaPipe Face Mesh ejecuta 100% en navegador (WebAssembly). Servidor recibe solo arrays numéricos 468×3.  
**Consecuencias:** (+) Cumplimiento regulatorio, latencia reducida. (-) Dependencia de compatibilidad de navegador, no control sobre calidad de cámara.

### ADR-002: V-JEPA 2 con pesos congelados + Predictor ligero
**Estado:** Aceptado  
**Contexto:** GPU A100/H100 no disponible para proyecto de grado. Fine-tuning completo de V-JEPA 2 requiere > 100 horas GPU.  
**Decisión:** X-Encoder congelado (inferencia en T4). Solo entrenar Predictor JEPA Compacto (38M params) con dataset propio.  
**Consecuencias:** (+) Viabilidad económica, reproducibilidad. (-) Capacidad limitada de adaptación a dominio facial específico (mitigado con RDL).

### ADR-003: SQLite para desarrollo, PostgreSQL para producción
**Estado:** Aceptado  
**Contexto:** Proyecto de grado no requiere alta concurrencia en fase de investigación.  
**Decisión:** SQLite en desarrollo (cero configuración). Migración a PostgreSQL via SQLAlchemy/Alembic si se escala.  
**Consecuencias:** (+) Simplicidad, portabilidad. (-) No apto para concurrencia alta en producción.

### ADR-004: Holm-Bonferroni sobre Bonferroni clásico
**Estado:** Aceptado  
**Contexto:** 4 hipótesis primarias con correlación esperada entre H1 y H4 (misma señal de entrada).  
**Decisión:** Holm-Bonferroni secuencial mantiene FWER ≤ 0.05 con mayor poder estadístico.  
**Consecuencias:** (+) Mayor poder, no requiere independencia. (-) Ligeramente más complejo de implementar/reportar.

---

## 5. Stack Tecnológico Detallado

| Capa | Tecnología | Versión | Rol |
|:---|:---|:---:|:---|
| Frontend | Vanilla JS + MediaPipe | 0.10.11 | Captura, FSP, demo |
| Backend | FastAPI + Uvicorn | 0.111.0 | API REST, WebSocket |
| ML | PyTorch + TorchVision | 2.3.0 | Embeddings, predictor |
| Datos | SQLAlchemy + Alembic | 2.0.30 | ORM, migraciones |
| Testing | pytest + Jest | 8.2.0 / 29.7.0 | Unit + integration |
| CI/CD | GitHub Actions | — | Lint, test, security |
| Colab | Google Colab T4 | — | Entrenamiento PJC |
| Docs | Markdown + Mermaid | — | Arquitectura, tesis |

---

## 6. Roadmap de Evolución Arquitectónica

| Sprint | Cambio Arquitectónico | Justificación |
|:---:|:---|:---|
| 1 | MediaPipe real en browser | Reemplazar placeholder de landmarks |
| 2 | Integrar X-Encoder V-JEPA 2 | Cargar pesos preentrenados en Colab |
| 3 | Entrenar PJC + calibrar θ | Dataset piloto (n=16) |
| 4 | Integrar RLM vía API | Análisis post-sesión con LLM |
| 5 | Docker Compose para staging | Preparar demo para jurados |

---

*Documento mantenido en `docs/ARCHITECTURE.md` — actualizar en cada Sprint Review*
