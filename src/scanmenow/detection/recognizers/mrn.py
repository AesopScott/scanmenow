"""
MedicalRecordRecognizer — HIPAA Safe Harbor identifier #8.

Detects medical record numbers (MRNs) using:
  - Prefixed patterns: "MRN: 7834291", "MR-ABC123", "Patient ID: 123456"
  - Context keywords boost score via AnalyzerEngine (+0.35)

Recall-biased: missing PHI is worse than a false positive.

Accepted false-positive surface (by design):
  - mrn_numeric (\\b\\d{6,10}\\b, score=0.25): requires context boost to reach
    THRESHOLD=0.5. Without a context keyword, bare 6-10 digit numbers (invoice
    IDs, order numbers, confirmation codes, date fragments) will not fire.
    With context, some non-MRN numbers will be flagged — this is acceptable.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "mrn",
    "medical record",
    "medical record number",
    "patient id",
    "patient number",
    "chart number",
    "chart #",
    "chart no",
    "record number",
    "record #",
]


class MedicalRecordRecognizer(PatternRecognizer):
    """Detect medical record numbers in clinical text."""

    PATTERNS = [
        # Explicitly prefixed: "MRN: 7834291", "MR-ABC1234", "MRN 123456"
        Pattern(
            name="mrn_prefixed",
            regex=r"\b(?:MRN|MR)[-:\s]{0,2}[A-Z0-9]{5,12}\b",
            score=0.75,
        ),
        # Context-anchored: 5-10 digit numeric (needs context boost to pass threshold)
        Pattern(
            name="mrn_numeric",
            regex=r"\b\d{6,10}\b",
            score=0.25,
        ),
        # Alphanumeric with dash: "AB-123456", "MED-7890123"
        Pattern(
            name="mrn_alphanumeric",
            regex=r"\b[A-Z]{1,4}-\d{5,9}\b",
            score=0.50,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="MEDICAL_RECORD_NUMBER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="MedicalRecordRecognizer",
        )
