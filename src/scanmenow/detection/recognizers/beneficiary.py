"""
HealthPlanBeneficiaryRecognizer — HIPAA Safe Harbor identifier #9.

Detects health plan beneficiary numbers:
  - Alphanumeric ID patterns (6-15 chars)
  - Context keywords required for low-confidence patterns

Recall-biased: missing PHI is worse than a false positive.

Accepted false-positive surface (by design):
  - beneficiary_numeric (\\b\\d{8,12}\\b, score=0.25): requires context boost to
    reach THRESHOLD=0.5. With beneficiary/insurance context, will match date
    strings (YYYYMMDD), order numbers, and other 8-12 digit values — acceptable.
  - beneficiary_alphanumeric (\\b[A-Z]{1,3}\\d{6,12}\\b, score=0.30): with context,
    will match product codes and reference IDs of similar format — acceptable.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "beneficiary",
    "beneficiary number",
    "beneficiary id",
    "member id",
    "member number",
    "plan id",
    "plan number",
    "insurance id",
    "insurance number",
    "subscriber id",
    "subscriber number",
    "group id",
    "group number",
    "policy number",
    "policy id",
    "coverage id",
    "enrollment id",
    "health plan",
]


class HealthPlanBeneficiaryRecognizer(PatternRecognizer):
    """Detect health plan beneficiary and member numbers in text."""

    PATTERNS = [
        # Explicit prefix: "Member ID: ABC123456", "Subscriber: 12345678"
        Pattern(
            name="beneficiary_prefixed",
            regex=r"\b(?:MEM|SUB|BEN|INS|POL|GRP)[A-Z0-9]{6,12}\b",
            score=0.70,
        ),
        # Alphanumeric ID 8-15 chars (needs context to pass threshold)
        Pattern(
            name="beneficiary_alphanumeric",
            regex=r"\b[A-Z]{1,3}\d{6,12}\b",
            score=0.30,
        ),
        # Numeric-only 8-12 digit (needs context to pass threshold)
        Pattern(
            name="beneficiary_numeric",
            regex=r"\b\d{8,12}\b",
            score=0.25,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="HEALTH_PLAN_BENEFICIARY",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="HealthPlanBeneficiaryRecognizer",
        )
