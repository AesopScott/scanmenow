"""
Audit Presidio's built-in entity types against HIPAA Safe Harbor identifiers.

Run with: uv run python scripts/audit_hipaa_coverage.py

Prints every entity type Presidio registers at AnalyzerEngine init time,
so the coverage matrix in docs/hipaa_coverage.json can be kept accurate.
"""

from presidio_analyzer import AnalyzerEngine


def list_presidio_entities() -> list[str]:
    """Return sorted list of all entity types Presidio supports by default."""
    engine = AnalyzerEngine()
    entities: set[str] = set()
    for recognizer in engine.registry.recognizers:
        entities.update(recognizer.supported_entities)
    return sorted(entities)


def main() -> None:
    entities = list_presidio_entities()
    print(f"Presidio supports {len(entities)} built-in entity types:\n")
    for entity in entities:
        print(f"  {entity}")

    print("\nCross-reference against 18 HIPAA Safe Harbor identifiers:")
    hipaa_map = {
        "Names": "PERSON",
        "Geographic data (< state)": "LOCATION",
        "Dates (except year)": "DATE_TIME",
        "Phone numbers": "PHONE_NUMBER",
        "Fax numbers": "PHONE_NUMBER (shared)",
        "Email addresses": "EMAIL_ADDRESS",
        "Social security numbers": "US_SSN",
        "Medical record numbers": "❌ custom needed",
        "Health plan beneficiary numbers": "❌ custom needed",
        "Account numbers": "US_BANK_NUMBER (partial) + ❌ custom needed",
        "Certificate/license numbers": "MEDICAL_LICENSE + US_DRIVER_LICENSE (partial) + ❌ custom needed",
        "Vehicle identifiers (VINs)": "❌ custom needed",
        "Device identifiers": "❌ custom needed",
        "Web URLs": "URL",
        "IP addresses": "IP_ADDRESS",
        "Biometric identifiers": "❌ custom needed (best-effort)",
        "Full-face photographs": "⊘ out of scope (text scanner)",
        "Any other unique ID": "⊘ catch-all (not directly detectable)",
    }
    for identifier, coverage in hipaa_map.items():
        print(f"  {identifier}: {coverage}")


if __name__ == "__main__":
    main()
