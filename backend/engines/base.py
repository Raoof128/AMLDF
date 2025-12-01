from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class AttackBase(ABC):
    """Abstract base class for all adversarial attacks."""

    @abstractmethod
    def run(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Execute the attack.

        Args:
            input_data: The input to be attacked (tensor, text, etc.).
            **kwargs: Attack-specific parameters (e.g., epsilon, target).

        Returns:
            A dictionary containing the adversarial example and metadata.
        """
        pass


class DefenseBase(ABC):
    """Abstract base class for all defense mechanisms."""

    @abstractmethod
    def apply(self, input_data: Any, **kwargs) -> Any:
        """
        Apply the defense to the input data.

        Args:
            input_data: The input data to defend.
            **kwargs: Defense-specific parameters.

        Returns:
            The sanitized/defended data.
        """
        pass


class DetectorBase(ABC):
    """Abstract base class for all attack/drift detectors."""

    @abstractmethod
    def detect(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Detect anomalies or attacks in the input data.

        Args:
            input_data: The input data to analyze.
            **kwargs: Detector-specific parameters.

        Returns:
            A dictionary containing detection results (e.g., is_attack, score).
        """
        pass
