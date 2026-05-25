"""
Tests for Task #3 custom HIPAA Safe Harbor PatternRecognizers.

Proof Unit 2 (PU2):
  MedicalRecordRecognizer, VehicleIdentifierRecognizer, HealthPlanBeneficiaryRecognizer
  Run: uv run pytest tests/test_hipaa_recognizers.py -k "mrn or vehicle or beneficiary" -v
  Expected: 6 passed

Proof Unit 3 (PU3):
  AccountNumberRecognizer, CertificateLicenseRecognizer, DeviceIdentifierRecognizer,
  BiometricIdentifierRecognizer
  Run: uv run pytest tests/test_hipaa_recognizers.py -k "account or license or device or biometric" -v
  Expected: 8 passed

Proof Unit 4 (PU4):
  AnalyzerEngine multi-entity integration
  Run: uv run pytest tests/test_hipaa_recognizers.py::test_analyzer_detects_multiple_entities -v
  Expected: 1 passed — >= 5 distinct entity types detected
"""

import pytest
from presidio_analyzer import AnalyzerEngine

from scanmenow.detection.recognizers import ALL_RECOGNIZERS

# ---------------------------------------------------------------------------
# Score threshold used in all tests — recall-biased; matches the docs spec
# ---------------------------------------------------------------------------
THRESHOLD = 0.5


# ---------------------------------------------------------------------------
# Shared engine fixture (session-scoped for performance)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def hipaa_engine() -> AnalyzerEngine:
    """AnalyzerEngine with all 7 custom HIPAA recognizers registered."""
    engine = AnalyzerEngine()
    for recognizer in ALL_RECOGNIZERS:
        engine.registry.add_recognizer(recognizer)
    return engine


def _find(hipaa_engine: AnalyzerEngine, text: str, entity_type: str) -> list:
    """Return findings for a specific entity_type above the score threshold."""
    results = hipaa_engine.analyze(
        text=text, language="en", score_threshold=THRESHOLD
    )
    return [r for r in results if r.entity_type == entity_type]


# ===========================================================================
# PU2 — Structured-format recognizers
# ===========================================================================


# ---------------------------------------------------------------------------
# MEDICAL_RECORD_NUMBER (HIPAA #8)
# ---------------------------------------------------------------------------


def test_mrn_positive(hipaa_engine: AnalyzerEngine) -> None:
    """MRN: prefixed numeric is detected."""
    text = "Patient medical record number MRN: 7834291 was flagged for review."
    findings = _find(hipaa_engine, text, "MEDICAL_RECORD_NUMBER")
    assert len(findings) >= 1, f"Expected MRN detection, got: {findings}"


def test_mrn_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Plain clinical prose without MRN patterns is not detected."""
    text = "The patient is scheduled for discharge tomorrow morning after recovery."
    findings = _find(hipaa_engine, text, "MEDICAL_RECORD_NUMBER")
    assert len(findings) == 0, f"Unexpected MRN detection: {findings}"


# ---------------------------------------------------------------------------
# VEHICLE_IDENTIFIER (HIPAA #12)
# ---------------------------------------------------------------------------


def test_vehicle_positive(hipaa_engine: AnalyzerEngine) -> None:
    """17-character NHTSA VIN is detected."""
    text = "The registered vehicle VIN 1HGBH41JXMN109186 belongs to the patient."
    findings = _find(hipaa_engine, text, "VEHICLE_IDENTIFIER")
    assert len(findings) >= 1, f"Expected VIN detection, got: {findings}"


def test_vehicle_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Plain clinical prose without VIN-like sequences is not detected."""
    text = "The family arrived by taxi and were greeted by the nursing staff on arrival."
    findings = _find(hipaa_engine, text, "VEHICLE_IDENTIFIER")
    assert len(findings) == 0, f"Unexpected vehicle detection: {findings}"


# ---------------------------------------------------------------------------
# HEALTH_PLAN_BENEFICIARY (HIPAA #9)
# ---------------------------------------------------------------------------


def test_beneficiary_positive(hipaa_engine: AnalyzerEngine) -> None:
    """Beneficiary-prefixed ID is detected with context keyword."""
    text = "The patient's beneficiary number is BEN987654321 according to the health plan."
    findings = _find(hipaa_engine, text, "HEALTH_PLAN_BENEFICIARY")
    assert len(findings) >= 1, f"Expected beneficiary detection, got: {findings}"


def test_beneficiary_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Plain clinical prose without beneficiary IDs is not detected."""
    text = "The patient has been enrolled in the wellness program since last spring."
    findings = _find(hipaa_engine, text, "HEALTH_PLAN_BENEFICIARY")
    assert len(findings) == 0, f"Unexpected beneficiary detection: {findings}"


# ===========================================================================
# PU3 — Context-anchored recognizers
# ===========================================================================


# ---------------------------------------------------------------------------
# ACCOUNT_NUMBER (HIPAA #10 supplemental)
# ---------------------------------------------------------------------------


def test_account_positive(hipaa_engine: AnalyzerEngine) -> None:
    """Numeric account number is detected when 'account number' context is present."""
    text = "Patient account number 123456789 is on file with the billing department."
    findings = _find(hipaa_engine, text, "ACCOUNT_NUMBER")
    assert len(findings) >= 1, f"Expected account detection, got: {findings}"


def test_account_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Financial prose without a qualifying account number is not detected."""
    text = "The billing department will contact you about your outstanding balance."
    findings = _find(hipaa_engine, text, "ACCOUNT_NUMBER")
    assert len(findings) == 0, f"Unexpected account detection: {findings}"


# ---------------------------------------------------------------------------
# CERTIFICATE_LICENSE_NUMBER (HIPAA #11 supplemental)
# ---------------------------------------------------------------------------


def test_license_positive(hipaa_engine: AnalyzerEngine) -> None:
    """DEA-format license number is detected with DEA context keyword."""
    text = "Provider DEA number AB1234567 is on record with the pharmacy."
    findings = _find(hipaa_engine, text, "CERTIFICATE_LICENSE_NUMBER")
    assert len(findings) >= 1, f"Expected license detection, got: {findings}"


def test_license_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Medical prose without any license identifier is not detected."""
    text = "The attending physician reviewed the treatment plan carefully and thoroughly."
    findings = _find(hipaa_engine, text, "CERTIFICATE_LICENSE_NUMBER")
    assert len(findings) == 0, f"Unexpected license detection: {findings}"


# ---------------------------------------------------------------------------
# DEVICE_IDENTIFIER (HIPAA #13)
# ---------------------------------------------------------------------------


def test_device_positive(hipaa_engine: AnalyzerEngine) -> None:
    """SN-prefixed device serial number is detected with serial context."""
    text = "Device serial number SN: ABC12345678 was logged before the procedure."
    findings = _find(hipaa_engine, text, "DEVICE_IDENTIFIER")
    assert len(findings) >= 1, f"Expected device detection, got: {findings}"


def test_device_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Equipment prose without any serial number is not detected."""
    text = "The infusion pump was checked and calibrated before the procedure began."
    findings = _find(hipaa_engine, text, "DEVICE_IDENTIFIER")
    assert len(findings) == 0, f"Unexpected device detection: {findings}"


# ---------------------------------------------------------------------------
# BIOMETRIC_IDENTIFIER (HIPAA #16)
# ---------------------------------------------------------------------------


def test_biometric_positive(hipaa_engine: AnalyzerEngine) -> None:
    """'Fingerprints' keyword is detected as a biometric identifier."""
    text = "The patient's fingerprints were collected for identification purposes."
    findings = _find(hipaa_engine, text, "BIOMETRIC_IDENTIFIER")
    assert len(findings) >= 1, f"Expected biometric detection, got: {findings}"


def test_biometric_negative(hipaa_engine: AnalyzerEngine) -> None:
    """Routine clinical prose without biometric keywords is not detected."""
    text = "The patient completed a routine blood pressure reading and vision screening."
    findings = _find(hipaa_engine, text, "BIOMETRIC_IDENTIFIER")
    assert len(findings) == 0, f"Unexpected biometric detection: {findings}"


# ===========================================================================
# PU4 — AnalyzerEngine multi-entity integration
# ===========================================================================


def test_analyzer_detects_multiple_entities(hipaa_engine: AnalyzerEngine) -> None:
    """
    A single PHI-rich text triggers >= 5 distinct entity types.

    Expected detections:
      PERSON                — John Smith (spaCy NER)
      EMAIL_ADDRESS         — john.smith@hospital.org
      US_SSN                — 123-45-6789
      MEDICAL_RECORD_NUMBER — MRN: 7834291
      VEHICLE_IDENTIFIER    — 1HGBH41JXMN109186
      PHONE_NUMBER          — 555-867-5309
    """
    text = (
        "Patient John Smith (john.smith@hospital.org) has SSN 123-45-6789. "
        "His medical record MRN: 7834291 was updated today. "
        "The registered vehicle VIN 1HGBH41JXMN109186 belongs to the patient. "
        "Call 555-867-5309 for appointment details."
    )
    results = hipaa_engine.analyze(
        text=text, language="en", score_threshold=THRESHOLD
    )
    distinct_types = {r.entity_type for r in results}

    assert len(distinct_types) >= 5, (
        f"Expected >= 5 distinct entity types, got {len(distinct_types)}: "
        f"{sorted(distinct_types)}"
    )
