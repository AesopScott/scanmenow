"""
Audit Presidio's built-in entity types against HIPAA Safe Harbor identifiers.

Run with: uv run python scripts/audit_hipaa_coverage.py

Prints every entity type Presidio registers at AnalyzerEngine init time,
so the coverage matrix in docs/hipaa_coverage.json can be kept accurate.

NOTE: list_presidio_entities() intentionally uses the bare AnalyzerEngine
(without custom recognizers) to enumerate what Presidio natively supports out
of the box. The cross-reference table below reflects the full project coverage
including custom recognizers added in Task #3. To enumerate all registered
entity types including custom ones at runtime, use build_analyzer() from
scanmenow.detection.analyzer instead.
"""

from presidio_analyzer import AnalyzerEngine


def list_presidio_entities() -> list[str]:
    """Return sorted list of all entity types Presidio supports by default (native only)."""
    engine = AnalyzerEngine()
    entities: set[str] = set()
    for recognizer in engine.registry.recognizers:
        entities.update(recognizer.supported_entities)
    return sorted(entities)


def main() -> None:
    entities = list_presidio_entities()
    print(f"Presidio supports {len(entities)} built-in entity types (native only):\n")
    for entity in entities:
        print(f"  {entity}")

    print("\nCross-reference against 18 HIPAA Safe Harbor identifiers (full project coverage):")
    hipaa_map = {
        "Names": "PERSON",
        "Geographic data (< state)": "LOCATION",
        "Dates (except year)": "DATE_TIME",
        "Phone numbers": "PHONE_NUMBER",
        "Fax numbers": "PHONE_NUMBER (shared)",
        "Email addresses": "EMAIL_ADDRESS",
        "Social security numbers": "US_SSN",
        "Medical record numbers": "✓ MEDICAL_RECORD_NUMBER (custom — MedicalRecordRecognizer)",
        "Health plan beneficiary numbers": "✓ HEALTH_PLAN_BENEFICIARY (custom — HealthPlanBeneficiaryRecognizer)",
        "Account numbers": "US_BANK_NUMBER (partial) + ✓ ACCOUNT_NUMBER (custom — AccountNumberRecognizer)",
        "Certificate/license numbers": "MEDICAL_LICENSE + US_DRIVER_LICENSE (partial) + ✓ CERTIFICATE_LICENSE_NUMBER (custom — CertificateLicenseRecognizer)",
        "Vehicle identifiers (VINs)": "✓ VEHICLE_IDENTIFIER (custom — VehicleIdentifierRecognizer)",
        "Device identifiers": "✓ DEVICE_IDENTIFIER (custom — DeviceIdentifierRecognizer)",
        "Web URLs": "URL",
        "IP addresses": "IP_ADDRESS",
        "Biometric identifiers": "✓ BIOMETRIC_IDENTIFIER (custom — BiometricIdentifierRecognizer, best-effort)",
        "Full-face photographs": "⊘ out of scope (text scanner)",
        "Any other unique ID": "⊘ catch-all (not directly detectable)",
    }
    for identifier, coverage in hipaa_map.items():
        print(f"  {identifier}: {coverage}")


if __name__ == "__main__":
    main()
