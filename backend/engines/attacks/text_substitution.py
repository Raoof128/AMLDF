import random
from typing import Any, Dict, List, Tuple

from backend.engines.base import AttackBase
from backend.utils.logger import logger

# Simple synonym dictionary for demonstration
SYNONYMS = {
    "good": ["great", "excellent", "superb", "fine"],
    "bad": ["terrible", "awful", "poor", "dreadful"],
    "happy": ["joyful", "cheerful", "content", "delighted"],
    "sad": ["unhappy", "sorrowful", "depressed", "down"],
    "fast": ["quick", "rapid", "swift", "speedy"],
    "slow": ["sluggish", "leisurely", "unhurried"],
    "smart": ["intelligent", "clever", "bright", "sharp"],
    "stupid": ["foolish", "dumb", "dense", "silly"],
}


class SynonymSubstitutionAttack(AttackBase):
    """
    NLP Attack that substitutes words with their synonyms.
    """

    def run(  # type: ignore[override]
        self, input_data: str, perturbation_rate: float = 0.3
    ) -> Dict[str, Any]:
        """
        Execute the synonym substitution attack.

        Args:
            input_data: The input text string.
            perturbation_rate: Probability of replacing a word (0.0 to 1.0).

        Returns:
            Dict containing:
                - adversarial_text: The modified text.
                - changes: List of (original, new) word tuples.
                - perturbation_rate: The rate used.
        """
        try:
            if not input_data:
                return {
                    "adversarial_text": "",
                    "changes": [],
                    "perturbation_rate": perturbation_rate,
                }

            words = input_data.split()
            new_words = []
            changes: List[Tuple[str, str]] = []

            for word in words:
                lower_word = word.lower()
                # Check if word has synonyms and if we should replace it
                if lower_word in SYNONYMS and random.random() < perturbation_rate:
                    synonym = random.choice(SYNONYMS[lower_word])

                    # Match case roughly
                    if word.istitle():
                        synonym = synonym.title()
                    elif word.isupper():
                        synonym = synonym.upper()

                    new_words.append(synonym)
                    changes.append((word, synonym))
                else:
                    new_words.append(word)

            adversarial_text = " ".join(new_words)

            logger.info(f"Synonym attack executed. {len(changes)} words changed.")

            return {
                "adversarial_text": adversarial_text,
                "changes": changes,
                "perturbation_rate": perturbation_rate,
            }

        except Exception as e:
            logger.error(f"Error during Synonym attack: {str(e)}")
            raise e


# Legacy functional interface
def synonym_substitution_attack(
    text: str, perturbation_rate: float = 0.3
) -> Tuple[str, List[Tuple[str, str]]]:
    attacker = SynonymSubstitutionAttack()
    result = attacker.run(text, perturbation_rate=perturbation_rate)
    return result["adversarial_text"], result["changes"]
