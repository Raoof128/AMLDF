from typing import Any, Dict

import torch

from backend.engines.base import DefenseBase
from backend.utils.logger import logger


class FeatureSqueezingDefense(DefenseBase):
    """
    Feature Squeezing Defense using Bit Depth Reduction.

    References:
        Xu, W., Evans, D., & Qi, Y. (2017).
        Feature Squeezing: Detecting Adversarial Examples in Deep Neural Networks.
    """

    def apply(  # type: ignore[override]
        self, input_data: torch.Tensor, bit_depth: int = 8
    ) -> torch.Tensor:
        """
        Apply bit depth reduction to the input data.

        Args:
            input_data: Input tensor (values usually in [0, 1]).
            bit_depth: Target bit depth (1-8).

        Returns:
            The squeezed (quantized) tensor.
        """
        try:
            if not 1 <= bit_depth <= 8:
                raise ValueError("Bit depth must be between 1 and 8.")

            max_val = (2**bit_depth) - 1

            # Quantize
            squeezed_data = torch.round(input_data * max_val) / max_val

            logger.info(f"Feature squeezing applied with bit_depth={bit_depth}")

            return squeezed_data

        except Exception as e:
            logger.error(f"Error during Feature Squeezing: {str(e)}")
            raise e


# Legacy functional interface
def bit_depth_reduction(data: torch.Tensor, bit_depth: int = 4) -> torch.Tensor:
    defender = FeatureSqueezingDefense()
    return defender.apply(data, bit_depth=bit_depth)
