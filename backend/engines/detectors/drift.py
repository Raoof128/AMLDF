from typing import Any, Dict, Optional

import numpy as np

from backend.engines.base import DetectorBase
from backend.utils.logger import logger


class DriftDetector(DetectorBase):
    """Statistical Drift Detector using Mean and Standard Deviation."""

    def __init__(self, reference_data: Optional[np.ndarray] = None):
        """
        Initialize the detector.

        Args:
            reference_data: Optional initial data to fit the detector.
        """
        self.reference_mean: Optional[np.ndarray] = None
        self.reference_std: Optional[np.ndarray] = None

        if reference_data is not None:
            self.fit(reference_data)

    def fit(self, data: np.ndarray) -> None:
        """
        Fit the detector on reference (clean) data.

        Args:
            data: Numpy array of shape (n_samples, n_features).
        """
        try:
            self.reference_mean = np.mean(data, axis=0)
            self.reference_std = np.std(data, axis=0)
            logger.info("Drift detector fitted successfully.")
        except Exception as e:
            logger.error(f"Error fitting drift detector: {str(e)}")
            raise e

    def detect(
        self, input_data: np.ndarray, threshold_sigma: float = 3.0
    ) -> Dict[str, Any]:
        """
        Detect if input_data drifts from reference.

        Args:
            input_data: New data batch to check.
            threshold_sigma: Threshold in standard deviations.

        Returns:
            Dict containing:
                - drift_score: The calculated distance/score.
                - is_drift: Boolean flag.
                - threshold: The threshold used.
        """
        if self.reference_mean is None:
            raise ValueError("Detector not fitted. Call fit() first.")

        try:
            current_mean = np.mean(input_data, axis=0)

            # Simple Euclidean distance between means
            distance = np.linalg.norm(current_mean - self.reference_mean)

            # Determine drift based on threshold
            is_drift = distance > threshold_sigma

            logger.info(
                f"Drift detection run. Score: {distance:.4f}, Drift: {is_drift}"
            )

            return {
                "drift_score": float(distance),
                "is_drift": bool(is_drift),
                "threshold": threshold_sigma,
            }
        except Exception as e:
            logger.error(f"Error during drift detection: {str(e)}")
            raise e
