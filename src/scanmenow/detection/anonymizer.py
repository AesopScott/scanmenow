"""Presidio Anonymizer wrapper — redacts detected PII/PHI entities."""

from typing import List
from presidio_analyzer import RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig


def build_anonymizer() -> AnonymizerEngine:
    """Create and return a configured AnonymizerEngine instance."""
    return AnonymizerEngine()


def anonymize_text(
    text: str,
    analyzer_results: List[RecognizerResult],
    anonymizer: AnonymizerEngine | None = None,
) -> str:
    """
    Redact detected PII/PHI entities in the given text.

    Replaces each detected entity with its entity type tag, e.g. <EMAIL_ADDRESS>.

    Args:
        text: The original text to anonymize.
        analyzer_results: Findings from analyze_text().
        anonymizer: Optional pre-built AnonymizerEngine; creates a new one if absent.

    Returns:
        Anonymized text with entities replaced by <ENTITY_TYPE> tags.
    """
    engine = anonymizer or build_anonymizer()
    result = engine.anonymize(
        text=text,
        analyzer_results=analyzer_results,
        operators={"DEFAULT": OperatorConfig("replace", {"new_value": None})},
    )
    return result.text
