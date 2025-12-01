from fastapi import APIRouter
from pydantic import BaseModel

from backend.engines.evaluation.threat_scorer import ThreatScorer

router = APIRouter()
scorer = ThreatScorer()


class ScoreRequest(BaseModel):
    attack_success: bool
    perturbation_norm: float
    confidence_drop: float
    attack_type: str


@router.post("/score")
async def calculate_threat_score(request: ScoreRequest):
    score = scorer.calculate_risk_score(
        request.attack_success, request.perturbation_norm, request.confidence_drop
    )
    report = scorer.generate_report(score, request.attack_type)
    return report
