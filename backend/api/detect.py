from typing import List

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.engines.detectors.drift import DriftDetector

router = APIRouter()

# Global detector for demo state
detector = DriftDetector()
# Fit with some random data initially
detector.fit(np.random.rand(100, 10))


class DetectRequest(BaseModel):
    data: List[List[float]]  # Batch of data


@router.post("/drift")
async def detect_drift(request: DetectRequest):
    try:
        new_data = np.array(request.data)
        result = detector.detect(new_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
