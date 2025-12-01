from typing import Any, Dict

import torch
import torch.nn.functional as F

from backend.engines.attacks.fgsm import FGSMAttack
from backend.engines.base import DefenseBase
from backend.utils.logger import logger


class AdversarialTrainingDefense(DefenseBase):
    """
    Simulated Adversarial Training.
    Fine-tunes a model on a batch of adversarial examples.
    """

    def __init__(self, model: torch.nn.Module):
        self.model = model
        self.attacker = FGSMAttack(model)
        self.optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    def apply(
        self, input_data: torch.Tensor, target: torch.Tensor, epochs: int = 1
    ) -> Dict[str, Any]:
        """
        Perform a training step using adversarial examples.

        Args:
            input_data: Batch of input images.
            target: Batch of labels.
            epochs: Number of training steps.

        Returns:
            Dict with training stats.
        """
        try:
            self.model.train()
            initial_loss = 0.0
            final_loss = 0.0

            for _ in range(epochs):
                # 1. Generate Adversarial Examples
                attack_result = self.attacker.run(input_data, target, epsilon=0.1)
                adv_data = attack_result["adversarial_data"]

                # 2. Train on Adversarial Examples
                self.optimizer.zero_grad()
                output = self.model(adv_data)
                loss = F.cross_entropy(output, target)
                loss.backward()
                self.optimizer.step()

                final_loss = loss.item()

            self.model.eval()
            logger.info(
                f"Adversarial training step complete. Final Loss: {final_loss:.4f}"
            )

            return {
                "defense": "Adversarial Training",
                "epochs": epochs,
                "final_loss": final_loss,
                "status": "Model weights updated",
            }

        except Exception as e:
            logger.error(f"Error during Adversarial Training: {str(e)}")
            raise e
