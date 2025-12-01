"""Threat scoring engine for AMLD-F."""

from typing import Any, Dict

from backend.utils.logger import logger


class ThreatScorer:
    """Engine for calculating threat scores and generating risk reports."""

    def calculate_risk_score(
        self, attack_success: bool, perturbation_norm: float, confidence_drop: float
    ) -> float:
        """
        Calculate a risk score (0-100) based on attack metrics.

        Args:
            attack_success: Whether the attack flipped the label.
            perturbation_norm: Magnitude of the perturbation (L2 norm or similar).
            confidence_drop: Drop in model confidence (0.0 to 1.0).

        Returns:
            A float representing the risk score (0 to 100).
        """
        try:
            score = 0.0

            if attack_success:
                score += 50.0

            # Higher confidence drop = higher risk (model was fooled easily)
            # Cap at 30 points
            score += min(confidence_drop * 100, 30.0)

            # Lower perturbation for success = higher risk (stealthy attack)
            if attack_success:
                if perturbation_norm < 0.05:
                    score += 20.0
                elif perturbation_norm < 0.1:
                    score += 10.0

            final_score = min(score, 100.0)
            logger.info(f"Risk score calculated: {final_score}")
            return final_score

        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            # Return a safe default or re-raise depending on policy. Re-raising for now.
            raise e

    def generate_report(self, risk_score: float, attack_type: str) -> Dict[str, Any]:
        """
        Generate a human-readable threat report.

        Args:
            risk_score: The calculated risk score (0-100).
            attack_type: The name of the attack (e.g., "FGSM").

        Returns:
            Dict containing severity, recommendation, etc.
        """
        severity = "Low"
        if risk_score > 75:
            severity = "High"
        elif risk_score > 40:
            severity = "Medium"

        return {
            "risk_score": risk_score,
            "severity": severity,
            "attack_type": attack_type,
            "recommendation": self._get_recommendation(severity, attack_type),
        }

    def _get_recommendation(self, severity: str, attack_type: str) -> str:
        """Generate recommendations based on severity."""
        if severity == "High":
            return (
                "Immediate mitigation required. "
                "Enable adversarial training and input sanitization."
            )
        elif severity == "Medium":
            return "Monitor closely. Consider enabling feature squeezing."
        return "Routine monitoring."
