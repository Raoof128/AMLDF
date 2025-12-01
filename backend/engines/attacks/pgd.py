from typing import Any, Dict

import torch
import torch.nn.functional as F

from backend.engines.base import AttackBase
from backend.utils.logger import logger


class PGDAttack(AttackBase):
    """
    Projected Gradient Descent (PGD) Attack.
    Iterative version of FGSM, generally considered a strong "first-order" attack.

    References:
        Madry, A., Makelov, A., Schmidt, L., & Tsipras, D., & Vladu, A. (2017).
        Towards Deep Learning Models Resistant to Adversarial Attacks.
    """

    def __init__(self, model: torch.nn.Module):
        self.model = model

    def run(
        self,
        input_data: torch.Tensor,
        target: torch.Tensor,
        epsilon: float = 0.3,
        alpha: float = 0.01,
        num_steps: int = 40,
    ) -> Dict[str, Any]:
        """
        Execute PGD Attack.

        Args:
            input_data: Input tensor (batch, channels, height, width).
            target: True label tensor.
            epsilon: Maximum perturbation (L-inf norm).
            alpha: Step size.
            num_steps: Number of iterations.

        Returns:
            Dict containing adversarial example and metadata.
        """
        try:
            data = input_data.clone().detach()
            # Random start (optional but recommended for PGD)
            data = data + torch.empty_like(data).uniform_(-epsilon, epsilon)
            data = torch.clamp(data, 0, 1)

            original_data = input_data.clone().detach()

            for _ in range(num_steps):
                data.requires_grad = True
                output = self.model(data)
                loss = F.cross_entropy(output, target)

                self.model.zero_grad()
                loss.backward()

                data_grad = data.grad.data

                # Update
                adv_data = data + alpha * data_grad.sign()

                # Project back to epsilon ball
                eta = torch.clamp(adv_data - original_data, -epsilon, epsilon)
                data = torch.clamp(original_data + eta, 0, 1).detach()

            perturbation = data - original_data

            logger.info(f"PGD attack executed. Steps: {num_steps}, Epsilon: {epsilon}")

            return {
                "adversarial_data": data,
                "perturbation": perturbation,
                "epsilon": epsilon,
                "steps": num_steps,
            }

        except Exception as e:
            logger.error(f"Error during PGD attack: {str(e)}")
            raise e
