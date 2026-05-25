"""
DeviceIdentifierRecognizer — HIPAA Safe Harbor identifier #13.

Detects medical device identifiers and equipment serial numbers.
High variability across manufacturers — recall-biased, context required.

Context keywords required to distinguish from generic numeric strings.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "serial",
    "serial number",
    "serial #",
    "serial no",
    "S/N",
    "SN:",
    "SN#",
    "device id",
    "device identifier",
    "device serial",
    "equipment id",
    "equipment serial",
    "asset id",
    "asset number",
    "instrument id",
    "model number",
    "lot number",
    "batch number",
    "UDI",
    "unique device identifier",
]


class DeviceIdentifierRecognizer(PatternRecognizer):
    """Detect medical device and equipment serial numbers in text."""

    PATTERNS = [
        # S/N or SN: prefix (high confidence with explicit marker)
        Pattern(
            name="device_sn_prefix",
            regex=r"\b(?:S/N|SN)[:\s#]{0,2}[A-Z0-9]{4,16}\b",
            score=0.70,
        ),
        # UDI-style: (01)NNNNNNNNNNNNN format
        Pattern(
            name="device_udi",
            regex=r"\(0[12]\)\d{13,14}",
            score=0.80,
        ),
        # Alphanumeric serial: "ABC-12345678" (needs context to pass threshold)
        Pattern(
            name="device_alphanumeric",
            regex=r"\b[A-Z]{1,5}[-]?\d{5,12}\b",
            score=0.30,
        ),
        # Numeric-only serial 6-15 digits (needs context to pass threshold)
        Pattern(
            name="device_numeric",
            regex=r"\b\d{6,15}\b",
            score=0.25,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="DEVICE_IDENTIFIER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="DeviceIdentifierRecognizer",
        )
