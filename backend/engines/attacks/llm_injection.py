from typing import Any, Dict, List

from backend.engines.base import AttackBase
from backend.utils.logger import logger

# Simulated database of "unsafe" patterns for educational purposes
JAILBREAK_PATTERNS = [
    "ignore previous instructions",
    "do anything now",
    "act as a developer mode",
    "always answer yes",
]

SAFE_RESPONSES = [
    "I cannot fulfill this request.",
    "I am programmed to be a helpful and harmless AI assistant.",
    "Sorry, but I can't help with that.",
]

UNSAFE_RESPONSE_SIMULATION = "Sure, here is how you might approach that..."


class LLMJailbreakSimulation(AttackBase):
    """
    Simulated LLM Jailbreak Attack for educational demonstration.
    Does NOT interact with real LLMs to ensure safety.
    """

    def run(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Simulate a jailbreak attempt.

        Args:
            prompt: The user input prompt.

        Returns:
            Dict containing the simulated response and success flag.
        """
        try:
            prompt_lower = prompt.lower()
            is_jailbreak = any(
                pattern in prompt_lower for pattern in JAILBREAK_PATTERNS
            )

            if is_jailbreak:
                response = UNSAFE_RESPONSE_SIMULATION
                success = True
                logger.warning(
                    f"Simulated Jailbreak SUCCESS for prompt: {prompt[:30]}..."
                )
            else:
                response = SAFE_RESPONSES[0]
                success = False
                logger.info(f"Simulated Jailbreak FAILED for prompt: {prompt[:30]}...")

            return {
                "original_prompt": prompt,
                "simulated_response": response,
                "success": success,
                "detected_patterns": [
                    p for p in JAILBREAK_PATTERNS if p in prompt_lower
                ],
            }

        except Exception as e:
            logger.error(f"Error during LLM simulation: {str(e)}")
            raise e
