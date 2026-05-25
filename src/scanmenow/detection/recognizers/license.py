"""
CertificateLicenseRecognizer — HIPAA Safe Harbor identifier #11 (supplemental).

Supplements Presidio's native MEDICAL_LICENSE and US_DRIVER_LICENSE with
broader recall for professional certificates, occupational licenses,
non-US licenses, and other credential numbers.

Context keywords required for broad alphanumeric patterns.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "license",
    "license number",
    "license #",
    "license no",
    "lic",
    "lic #",
    "certificate",
    "certificate number",
    "cert",
    "cert #",
    "credential",
    "credential number",
    "professional license",
    "occupational license",
    "state license",
    "registration number",
    "permit number",
    "permit #",
    "DEA",
    "NPI",
]


class CertificateLicenseRecognizer(PatternRecognizer):
    """Detect professional certificate and license numbers in text."""

    PATTERNS = [
        # DEA number format: 2 letters + 7 digits (high confidence)
        Pattern(
            name="dea_number",
            regex=r"\b[A-Z]{2}\d{7}\b",
            score=0.70,
        ),
        # NPI: 10-digit numeric starting with 1 or 2 (needs context to reach threshold)
        # Score intentionally below THRESHOLD=0.5 — requires NPI context keyword boost.
        # A 10-digit number starting with 1 or 2 is too broad to fire without context
        # (matches phone numbers, reference numbers, order IDs, etc.).
        Pattern(
            name="npi_number",
            regex=r"\b[12]\d{9}\b",
            score=0.30,
        ),
        # Alphanumeric 4-12 chars (needs context to pass threshold)
        Pattern(
            name="license_alphanumeric",
            regex=r"\b[A-Z]{1,4}[-]?\d{4,10}\b",
            score=0.30,
        ),
        # All-numeric 5-10 digits (needs context to pass threshold)
        Pattern(
            name="license_numeric",
            regex=r"\b\d{5,10}\b",
            score=0.25,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="CERTIFICATE_LICENSE_NUMBER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="CertificateLicenseRecognizer",
        )
