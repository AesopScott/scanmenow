"""Presidio Analyzer wrapper — detects PII/PHI entities in text."""

from typing import List
from presidio_analyzer import AnalyzerEngine, RecognizerResult


def build_analyzer() -> AnalyzerEngine:
    """Create and return a configured AnalyzerEngine instance."""
    return AnalyzerEngine()


def analyze_text(
    text: str,
    language: str = "en",
    analyzer: AnalyzerEngine | None = None,
) -> List[RecognizerResult]:
    """
    Detect PII/PHI entities in the given text.

    Args:
        text: The input text to analyze.
        language: Language code (default: 'en').
        analyzer: Optional pre-built AnalyzerEngine; creates a new one if absent.

    Returns:
        List of RecognizerResult with entity_type, start, end, score.
    """
    engine = analyzer or build_analyzer()
    return engine.analyze(text=text, language=language)
