from typing import List

import torch
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.engines.defences.adversarial_training import AdversarialTrainingDefense
from backend.engines.defences.feature_squeeze import FeatureSqueezingDefense
from backend.models.vision_model import get_vision_model
from backend.utils.logger import logger

router = APIRouter()

defender = FeatureSqueezingDefense()
# Initialize model for adv training
vision_model = get_vision_model()
adv_trainer = AdversarialTrainingDefense(vision_model)


class DefenseRequest(BaseModel):
    # For demo, we accept a list of floats representing a flattened image or similar
    data: List[float]
    bit_depth: int = 4


class AdvTrainingRequest(BaseModel):
    epochs: int = 1


@router.post("/feature_squeezing")
async def feature_squeezing_defense(request: DefenseRequest):
    try:
        # Convert list to tensor
        tensor_data = torch.tensor(request.data)

        # Apply defense
        defended_data = defender.apply(tensor_data, bit_depth=request.bit_depth)

        return {
            "defense": "Feature Squeezing (Bit Depth Reduction)",
            "original_sample": request.data[:5],  # Show first 5
            "defended_sample": defended_data.tolist()[:5],
            "bit_depth": request.bit_depth,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adversarial_training")
async def adversarial_training_defense(request: AdvTrainingRequest):
    try:
        # Generate dummy batch for demo (10 images)
        data = torch.rand(10, 1, 28, 28)
        target = torch.randint(0, 10, (10,))

        result = adv_trainer.apply(data, target, epochs=request.epochs)
        return result
    except Exception as e:
        logger.error(f"Error in Adv Training endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
