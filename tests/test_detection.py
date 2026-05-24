"""Smoke tests for detection core — Analyzer, Anonymizer, and spaCy NER."""

import time
import pytest
from scanmenow.detection.analyzer import analyze_text, build_analyzer
from scanmenow.detection.anonymizer import anonymize_text, build_anonymizer

SAMPLE_EMAIL_TEXT = "Please contact support@example.com for help."
SAMPLE_PERSON_TEXT = "Dr. John Smith reviewed the patient records."

# --- Shared fixtures ---

@pytest.fixture(scope="module")
def analyzer():
    return build_analyzer()


@pytest.fixture(scope="module")
def anonymizer():
    return build_anonymizer()


# --- PU2: Presidio Analyzer ---

def test_analyzer_detects_email(analyzer):
    """Analyzer detects EMAIL_ADDRESS with confidence >= 0.5."""
    results = analyze_text(SAMPLE_EMAIL_TEXT, analyzer=analyzer)
    email_findings = [r for r in results if r.entity_type == "EMAIL_ADDRESS"]
    assert len(email_findings) >= 1, f"Expected EMAIL_ADDRESS finding, got: {results}"
    assert email_findings[0].score >= 0.5


def test_analyzer_returns_span(analyzer):
    """Analyzer finding contains valid start/end offsets within the text."""
    results = analyze_text(SAMPLE_EMAIL_TEXT, analyzer=analyzer)
    email_findings = [r for r in results if r.entity_type == "EMAIL_ADDRESS"]
    assert len(email_findings) >= 1
    finding = email_findings[0]
    assert finding.start >= 0
    assert finding.end > finding.start
    assert finding.end <= len(SAMPLE_EMAIL_TEXT)


# --- PU3: Presidio Anonymizer ---

def test_anonymizer_redacts_email(analyzer, anonymizer):
    """Anonymizer replaces EMAIL_ADDRESS with a tag; original email not present."""
    results = analyze_text(SAMPLE_EMAIL_TEXT, analyzer=analyzer)
    anonymized = anonymize_text(SAMPLE_EMAIL_TEXT, results, anonymizer=anonymizer)
    assert "support@example.com" not in anonymized
    assert "<EMAIL_ADDRESS>" in anonymized


def test_anonymizer_preserves_non_pii(analyzer, anonymizer):
    """Non-PII text is preserved unchanged after anonymization."""
    results = analyze_text(SAMPLE_EMAIL_TEXT, analyzer=analyzer)
    anonymized = anonymize_text(SAMPLE_EMAIL_TEXT, results, anonymizer=anonymizer)
    assert "Please contact" in anonymized
    assert "for help." in anonymized


# --- PU4: spaCy NER ---

def test_spacy_detects_person():
    """spaCy en_core_web_lg loads and detects a PERSON entity in sample text."""
    import time
    from scanmenow.detection.ner import get_nlp, extract_entities

    start = time.perf_counter()
    entities = extract_entities(SAMPLE_PERSON_TEXT)
    elapsed = time.perf_counter() - start

    print(f"\n  spaCy entity extraction: {elapsed:.2f}s, found: {entities}")

    person_entities = [e for e in entities if e[1] == "PERSON"]
    assert len(person_entities) >= 1, (
        f"Expected at least one PERSON entity in '{SAMPLE_PERSON_TEXT}', got: {entities}"
    )


def test_spacy_model_caches():
    """Calling get_nlp() twice returns the same object (no double-load)."""
    from scanmenow.detection.ner import get_nlp
    nlp1 = get_nlp()
    nlp2 = get_nlp()
    assert nlp1 is nlp2
