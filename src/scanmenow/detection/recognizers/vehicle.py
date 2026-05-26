"""
VehicleIdentifierRecognizer — HIPAA Safe Harbor identifier #12.

Detects vehicle identifiers:
  - VINs: strict NHTSA 17-character format (excludes I, O, Q)
  - License plates: common US state formats
  - Context keywords boost score via AnalyzerEngine (+0.35)

High precision for VINs due to strict character-set and length constraint.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "vin",
    "vehicle identification",
    "vehicle identification number",
    "license plate",
    "plate number",
    "plate #",
    "tag number",
    "registration",
    "vehicle",
]


class VehicleIdentifierRecognizer(PatternRecognizer):
    """Detect VINs and license plate numbers in text."""

    PATTERNS = [
        # NHTSA VIN: 17 chars, excludes I (0x49), O (0x4F), Q (0x51)
        # Positions: WMI (3) + VDS (6) + VIS (8)
        Pattern(
            name="vin_standard",
            regex=r"\b[A-HJ-NPR-Z0-9]{17}\b",
            score=0.85,
        ),
        # US license plates: 1-3 letters + 3-4 digits, common formats
        Pattern(
            name="license_plate_us",
            regex=r"\b[A-Z]{1,3}[-\s]?\d{3,4}[-\s]?[A-Z]{0,3}\b",
            score=0.30,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="VEHICLE_IDENTIFIER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="VehicleIdentifierRecognizer",
        )
