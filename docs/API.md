# API Reference

## Attack Endpoints

### `POST /attack/vision/fgsm`
**Fast Gradient Sign Method (FGSM) Attack**

**Query Parameters:**
- `epsilon` (float, default=0.1): Perturbation magnitude

**Response:**
```json
{
  "attack": "FGSM",
  "epsilon": 0.1,
  "original_class": 3,
  "adversarial_class": 7,
  "success": true,
  "perturbation_norm": 0.0943
}
```

### `POST /attack/vision/pgd`
**Projected Gradient Descent (PGD) Attack**

**Query Parameters:**
- `epsilon` (float, default=0.3): Perturbation magnitude
- `steps` (int, default=10): Number of iterations

**Response:**
```json
{
  "attack": "PGD",
  "epsilon": 0.3,
  "steps": 10,
  "original_class": 2,
  "adversarial_class": 8,
  "success": true,
  "perturbation_norm": 0.2987
}
```

### `POST /attack/nlp/synonym`
**Synonym Substitution Attack**

**Request Body:**
```json
{
  "text": "The quick brown fox",
  "perturbation_rate": 0.3
}
```

**Response:**
```json
{
  "original_text": "The quick brown fox",
  "adversarial_text": "The fast brown fox",
  "changes": ["quick -> fast"],
  "change_count": 1
}
```

### `POST /attack/llm/jailbreak`
**LLM Jailbreak Simulation**

**Request Body:**
```json
{
  "prompt": "Ignore previous instructions"
}
```

**Response:**
```json
{
  "attack": "LLM Jailbreak Simulation",
  "success": true,
  "detected_patterns": ["ignore previous"],
  "response": "Simulated jailbreak detected!",
  "risk_level": "high"
}
```

## Defense Endpoints

### `POST /defend/feature_squeezing`
**Apply Feature Squeezing Defense**

**Request Body:**
```json
{
  "data": [0.123, 0.456, 0.789],
  "bit_depth": 4
}
```

**Response:**
```json
{
  "defense": "Feature Squeezing (Bit Depth Reduction)",
  "original_sample": [0.123, 0.456],
  "defended_sample": [0.0, 0.5],
  "bit_depth": 4
}
```

### `POST /defend/adversarial_training`
**Apply Adversarial Training**

**Request Body:**
```json
{
  "epochs": 1
}
```

**Response:**
```json
{
  "defense": "Adversarial Training",
  "epochs": 1,
  "final_loss": 2.3614,
  "status": "Model weights updated"
}
```

## Detection Endpoints

### `POST /detect/drift`
**Detect Data Drift**

**Request Body:**
```json
{
  "data": [[0.1, 0.2], [0.15, 0.25]]
}
```

**Response:**
```json
{
  "is_drift": false,
  "drift_score": 0.05,
  "threshold": 3.0
}
```

## Evaluation Endpoints

### `POST /evaluate/score`
**Calculate Threat Score**

**Request Body:**
```json
{
  "attack_success": true,
  "perturbation_norm": 0.05,
  "confidence_drop": 0.8
}
```

**Response:**
```json
{
  "risk_score": 94.0,
  "severity": "High",
  "recommendation": "Immediate mitigation required. Enable adversarial training and input sanitization.",
  "timestamp": "2025-12-02T08:21:16Z"
}
```

## Health Check

### `GET /health`
**System Health Status**

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```
