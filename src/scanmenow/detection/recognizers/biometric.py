"""
BiometricIdentifierRecognizer — HIPAA Safe Harbor identifier #16.

Best-effort text-description approach: detects mentions of biometric
identifiers as noun phrases. Cannot detect raw biometric data blobs
(binary fingerprint templates, voiceprint embeddings, etc.).

Documented limitation: high false-negative rate for non-descriptive
references. Do not apply accuracy thresholds to this identifier.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "biometric",
    "fingerprint",
    "voiceprint",
    "retina",
    "iris",
    "facial recognition",
    "face recognition",
    "palm print",
    "gait",
    "vein pattern",
]


class BiometricIdentifierRecognizer(PatternRecognizer):
    """Detect textual mentions of biometric identifiers."""

    PATTERNS = [
        # Fingerprint references
        Pattern(
            name="biometric_fingerprint",
            regex=r"\bfingerprint(?:s|ing|ed)?\b",
            score=0.65,
        ),
        # Voiceprint references
        Pattern(
            name="biometric_voiceprint",
            regex=r"\bvoiceprint(?:s)?\b",
            score=0.65,
        ),
        # Retina / iris scan
        Pattern(
            name="biometric_retina_iris",
            regex=r"\b(?:retina|iris)\s+scan(?:s|ning|ned)?\b",
            score=0.65,
        ),
        # Facial recognition
        Pattern(
            name="biometric_facial",
            regex=r"\bfacial\s+(?:recognition|scan|id)\b",
            score=0.65,
        ),
        # Biometric (generic keyword — lower confidence).
        # Note: "biometric" also appears in CONTEXT_WORDS, so every match of this
        # pattern triggers its own context boost, effectively making it fire above
        # threshold unconditionally. This is intentional for the best-effort
        # identifier (#16) — any mention of "biometric" in a document is worth
        # flagging regardless of surrounding context.
        Pattern(
            name="biometric_generic",
            regex=r"\bbiometric(?:s|ally)?\b",
            score=0.50,
        ),
        # Palm print
        Pattern(
            name="biometric_palm",
            regex=r"\bpalm\s+print(?:s)?\b",
            score=0.65,
        ),
        # Gait analysis
        Pattern(
            name="biometric_gait",
            regex=r"\bgait\s+(?:analysis|recognition|scan)\b",
            score=0.65,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="BIOMETRIC_IDENTIFIER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="BiometricIdentifierRecognizer",
        )
