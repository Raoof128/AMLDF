import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.engines.attacks.fgsm import FGSMAttack
from backend.engines.attacks.llm_injection import LLMJailbreakSimulation
from backend.engines.attacks.pgd import PGDAttack
from backend.engines.attacks.text_substitution import SynonymSubstitutionAttack
from backend.models.vision_model import get_vision_model
from backend.utils.logger import logger

router = APIRouter()

# Initialize model once for demo
vision_model = get_vision_model()
fgsm_attacker = FGSMAttack(vision_model)
pgd_attacker = PGDAttack(vision_model)
nlp_attacker = SynonymSubstitutionAttack()
llm_simulator = LLMJailbreakSimulation()


class NLPAttackRequest(BaseModel):
    text: str
    perturbation_rate: float = 0.3


class LLMAttackRequest(BaseModel):
    prompt: str


@router.post("/vision/fgsm")
async def vision_fgsm_attack(epsilon: float = 0.1):
    """
    Simulates an FGSM attack on a random noise image (for demo purposes).
    """
    try:
        # Generate random "image" (1, 1, 28, 28) for MNIST-like
        data = torch.rand(1, 1, 28, 28)
        # Fake target class
        target = torch.tensor([3])

        original_output = vision_model(data)
        original_pred = original_output.max(1, keepdim=True)[1]

        # Run Attack
        result = fgsm_attacker.run(data, target, epsilon=epsilon)
        adv_data = result["adversarial_data"]
        perturbation = result["perturbation"]

        adv_output = vision_model(adv_data)
        adv_pred = adv_output.max(1, keepdim=True)[1]

        success = original_pred.item() != adv_pred.item()

        return {
            "attack": "FGSM",
            "epsilon": epsilon,
            "original_class": int(original_pred.item()),
            "adversarial_class": int(adv_pred.item()),
            "success": success,
            "perturbation_norm": float(torch.norm(perturbation).item()),
        }
    except Exception as e:
        logger.error(f"Error in vision attack endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vision/pgd")
async def vision_pgd_attack(epsilon: float = 0.3, steps: int = 10):
    """
    Simulates a PGD attack on a random noise image.
    """
    try:
        data = torch.rand(1, 1, 28, 28)
        target = torch.tensor([3])

        original_output = vision_model(data)
        original_pred = original_output.max(1, keepdim=True)[1]

        result = pgd_attacker.run(data, target, epsilon=epsilon, num_steps=steps)
        adv_data = result["adversarial_data"]

        adv_output = vision_model(adv_data)
        adv_pred = adv_output.max(1, keepdim=True)[1]

        success = original_pred.item() != adv_pred.item()

        return {
            "attack": "PGD",
            "epsilon": epsilon,
            "steps": steps,
            "original_class": int(original_pred.item()),
            "adversarial_class": int(adv_pred.item()),
            "success": success,
            "perturbation_norm": float(torch.norm(result["perturbation"]).item()),
        }
    except Exception as e:
        logger.error(f"Error in PGD endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/nlp/synonym")
async def nlp_synonym_attack(request: NLPAttackRequest):
    try:
        result = nlp_attacker.run(
            request.text, perturbation_rate=request.perturbation_rate
        )
        return {
            "original_text": request.text,
            "adversarial_text": result["adversarial_text"],
            "changes": result["changes"],
            "change_count": len(result["changes"]),
        }
    except Exception as e:
        logger.error(f"Error in NLP attack endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/llm/jailbreak")
async def llm_jailbreak_attack(request: LLMAttackRequest):
    try:
        result = llm_simulator.run(request.prompt)
        return result
    except Exception as e:
        logger.error(f"Error in LLM endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
