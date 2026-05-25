"""
AccountNumberRecognizer — HIPAA Safe Harbor identifier #10 (supplemental).

Supplements Presidio's native US_BANK_NUMBER with broader recall for
non-bank accounts: utility, retail, medical billing, patient financial.

Context keywords required to distinguish from other number sequences.
"""

from presidio_analyzer import Pattern, PatternRecognizer

CONTEXT_WORDS = [
    "account",
    "account number",
    "account #",
    "account no",
    "acct",
    "acct #",
    "acct no",
    "billing account",
    "patient account",
    "financial account",
    "utility account",
    "customer account",
    "reference number",
    "invoice number",
]


class AccountNumberRecognizer(PatternRecognizer):
    """Detect non-bank account numbers in text."""

    PATTERNS = [
        # Numeric 6-16 digits (requires context boost to reach threshold)
        Pattern(
            name="account_numeric",
            regex=r"\b\d{6,16}\b",
            score=0.25,
        ),
        # Alphanumeric with optional dash/hyphen: "ACC-789012", "12345-678"
        Pattern(
            name="account_alphanumeric",
            regex=r"\b[A-Z0-9]{3,6}[-]\d{4,10}\b",
            score=0.40,
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            supported_entity="ACCOUNT_NUMBER",
            patterns=self.PATTERNS,
            context=CONTEXT_WORDS,
            supported_language="en",
            name="AccountNumberRecognizer",
        )
