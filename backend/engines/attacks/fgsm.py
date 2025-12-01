from typing import Any, Dict, Tuple

import torch
import torch.nn.functional as F

from backend.engines.base import AttackBase
from backend.utils.logger import logger


class FGSMAttack(AttackBase):
    """
    Fast Gradient Sign Method (FGSM) Attack.

    References:
        Goodfellow, I. J., Shlens, J., & Szegedy, C. (2014).
        Explaining and harnessing adversarial examples.
    """

    def __init__(self, model: torch.nn.Module):
        """
        Initialize the FGSM attack.

        Args:
            model: The PyTorch model to attack.
        """
        self.model = model

    def run(
        self, input_data: torch.Tensor, target: torch.Tensor, epsilon: float = 0.1
    ) -> Dict[str, Any]:
        """
        Execute the FGSM attack.

        Args:
            input_data: Input tensor (batch, channels, height, width).
            target: True label tensor.
            epsilon: Perturbation magnitude.

        Returns:
            Dict containing:
                - adversarial_data: The perturbed input.
                - perturbation: The noise added.
                - epsilon: The epsilon used.
        """
        try:
            # Ensure input requires grad
            data = input_data.clone().detach()
            data.requires_grad = True

            # Forward pass
            output = self.model(data)
            loss = F.cross_entropy(output, target)

            # Zero gradients
            self.model.zero_grad()

            # Backward pass
            loss.backward()

            # Collect data gradient
            data_grad = data.grad.data

            # Create perturbation
            sign_data_grad = data_grad.sign()
            perturbation = epsilon * sign_data_grad

            # Create adversarial example
            perturbed_data = data + perturbation

            # Clamp to valid image range [0, 1]
            perturbed_data = torch.clamp(perturbed_data, 0, 1)

            logger.info(f"FGSM attack executed with epsilon={epsilon}")

            return {
                "adversarial_data": perturbed_data,
                "perturbation": perturbation,
                "epsilon": epsilon,
            }

        except Exception as e:
            logger.error(f"Error during FGSM attack: {str(e)}")
            raise e


# Helper function for backward compatibility or simple usage
def fgsm_attack(
    model: torch.nn.Module,
    data: torch.Tensor,
    target: torch.Tensor,
    epsilon: float = 0.1,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Legacy functional interface for FGSM.
    """
    attacker = FGSMAttack(model)
    result = attacker.run(data, target, epsilon)
    return result["adversarial_data"], result["perturbation"]
