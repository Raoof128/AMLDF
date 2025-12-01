# Architecture Overview

## System Design

AMLD-F is designed as a modular, service-oriented architecture to facilitate the simulation, detection, and mitigation of adversarial attacks on machine learning models.

### High-Level Components

1.  **API Layer (FastAPI)**:
    *   Serves as the entry point for all interactions.
    *   Routes requests to appropriate engines (Attack, Defense, Detection).
    *   Handles input validation and response formatting.

2.  **Core Engines**:
    *   **Attack Engine**: Contains implementations of adversarial attacks (FGSM, PGD, etc.). Inherits from `AttackBase`.
    *   **Defense Engine**: Implements defense mechanisms (Feature Squeezing, Adversarial Training). Inherits from `DefenseBase`.
    *   **Detection Engine**: Monitors data for drift and anomalies. Inherits from `DetectorBase`.
    *   **Evaluation Engine**: Calculates threat scores and generates reports.

3.  **Model Registry**:
    *   Manages the lifecycle of ML models (Vision, NLP, Tabular).
    *   Provides a unified interface for model inference.

4.  **Frontend Dashboard**:
    *   Lightweight HTML/JS interface for real-time interaction.
    *   Visualizes attack results, perturbations, and defense effectiveness.

### Data Flow

1.  **Attack Simulation**:
    `User Request -> API -> Attack Engine -> Model -> Result (Adversarial Example)`

2.  **Defense Application**:
    `Adversarial Example -> API -> Defense Engine -> Sanitized Input -> Model -> Result (Prediction)`

3.  **Drift Detection**:
    `Input Batch -> API -> Detection Engine -> Drift Score -> Alert`

## Security Considerations

*   **Sandboxing**: All attacks are executed in memory or on isolated synthetic data.
*   **Input Validation**: Strict Pydantic models ensure only valid data reaches the engines.
*   **No External Calls**: The system is self-contained and does not make unauthorized external network requests.
