# Presidio Entity Type Registry

Every Presidio entity type string used in this project. For each: how it's produced (built-in Presidio recognizer or custom `PatternRecognizer`), where it's consumed (test assertions, `findings.entity_type` column), and status. Update whenever a new recognizer is added or an entity type string is referenced in tests or storage logic.

**Cross-boundary contract:** `findings.entity_type` (SQLite column) stores these strings verbatim. Test assertions compare against them. Custom recognizers must register the exact string that tests assert — a mismatch causes silent misses.

---

## `EMAIL_ADDRESS`

Standard email address (RFC 5322). Detected by Presidio's built-in `EmailRecognizer`.

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.EmailRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in) — registers `EmailRecognizer` automatically

**Consumers**
- `tests/test_detection.py:28` — `r.entity_type == "EMAIL_ADDRESS"` (Proof Unit 2)
- `tests/test_detection.py:36` — filter for email findings in span test
- `tests/test_detection.py:47` — anonymizer redaction tag `<EMAIL_ADDRESS>` (Proof Unit 3)
- `tests/test_storage.py:24` — `Finding(entity_type="EMAIL_ADDRESS", ...)` (Proof Unit 5)
- `tests/test_storage.py:33` — order assertion `results[1].entity_type == "EMAIL_ADDRESS"`
- `tests/test_storage.py:41` — `Finding(entity_type="EMAIL_ADDRESS", ...)` (CSV export test)
- `src/scanmenow/storage/db.py:55` — `entity_type TEXT NOT NULL` column in `findings`

**Status:** ✓ native — wired and smoke-tested

---

## `PERSON`

Full name of an individual. Detected by Presidio's spaCy-backed `SpacyRecognizer` using `en_core_web_lg`.

**Source:** Presidio built-in (native, via spaCy NER)
**Recognizer:** `presidio_analyzer.predefined_recognizers.SpacyRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in) — registers `SpacyRecognizer` automatically

**Consumers**
- `tests/test_detection.py:75` — `e[1] == "PERSON"` in spaCy NER smoke test (Proof Unit 4)
- `tests/test_storage.py:25` — `Finding(entity_type="PERSON", ...)` (Proof Unit 5)
- `tests/test_storage.py:32` — order assertion `results[0].entity_type == "PERSON"`
- `tests/test_storage.py:42` — `Finding(entity_type="PERSON", ...)` (CSV export test)

**Status:** ✓ native — wired and smoke-tested

---

## `PHONE_NUMBER`

Phone number in common US/international formats. Covers fax numbers (no separate HIPAA Safe Harbor recognizer needed).

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.PhoneRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed here for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `US_SSN`

US Social Security Number. Detected by Presidio's built-in `UsSsnRecognizer`.

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.UsSsnRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `IP_ADDRESS`

IPv4 and IPv6 addresses.

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.IpRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `URL`

Web URLs and domain names.

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.UrlRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `LOCATION`

Geographic location (smaller than state — covers HIPAA Safe Harbor geographic data identifier).

**Source:** Presidio built-in (native, via spaCy NER)
**Recognizer:** `presidio_analyzer.predefined_recognizers.SpacyRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `DATE_TIME`

Dates and times (covers HIPAA Safe Harbor dates except year — birth dates, admission dates, etc.).

**Source:** Presidio built-in (native)
**Recognizer:** `presidio_analyzer.predefined_recognizers.DateRecognizer`

**Producers**
- Presidio `AnalyzerEngine` (built-in)

**Consumers**
- None yet in tests — listed for HIPAA Safe Harbor coverage completeness (Task #3 audit)

**Status:** ✓ native — not yet asserted in tests; confirmed covered per Task #3 gap analysis

---

## `MEDICAL_RECORD_NUMBER`

Medical Record Number (MRN) — HL7-style alphanumeric identifiers with context keywords ("MRN", "medical record", "patient ID").

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/mrn.py` — `MedicalRecordRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/mrn.py:53` — `supported_entity="MEDICAL_RECORD_NUMBER"` (3 patterns: prefixed, numeric, alphanumeric)
- `src/scanmenow/detection/recognizers/__init__.py:31` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:67` — `_find(..., "MEDICAL_RECORD_NUMBER")` positive assertion
- `tests/test_hipaa_recognizers.py:74` — `_find(..., "MEDICAL_RECORD_NUMBER")` negative assertion
- `tests/test_hipaa_recognizers.py:228` — counted in multi-entity integration test

**Status:** ✓ implemented and tested (Task #3)

---

## `HEALTH_PLAN_BENEFICIARY`

Health plan beneficiary number / member ID — health plan ID patterns with context keywords ("beneficiary", "member ID", "plan ID").

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/beneficiary.py` — `HealthPlanBeneficiaryRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/beneficiary.py:61` — `supported_entity="HEALTH_PLAN_BENEFICIARY"` (3 patterns: prefixed, alphanumeric, numeric)
- `src/scanmenow/detection/recognizers/__init__.py:32` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:105` — `_find(..., "HEALTH_PLAN_BENEFICIARY")` positive assertion
- `tests/test_hipaa_recognizers.py:112` — `_find(..., "HEALTH_PLAN_BENEFICIARY")` negative assertion

**Status:** ✓ implemented and tested (Task #3)

---

## `ACCOUNT_NUMBER`

Generic financial account number — numeric patterns with context keywords ("account", "acct", "account number"). Recall-biased; some false positives acceptable. Supplements native `US_BANK_NUMBER`.

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/account.py` — `AccountNumberRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/account.py:50` — `supported_entity="ACCOUNT_NUMBER"` (2 patterns: numeric, alphanumeric)
- `src/scanmenow/detection/recognizers/__init__.py:33` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:129` — `_find(..., "ACCOUNT_NUMBER")` positive assertion
- `tests/test_hipaa_recognizers.py:136` — `_find(..., "ACCOUNT_NUMBER")` negative assertion

**Status:** ✓ implemented and tested (Task #3)

---

## `CERTIFICATE_LICENSE_NUMBER`

Certificate or license number — alphanumeric patterns with context keywords ("license", "certificate", "cert", "credential"). Recall-biased. Supplements native `MEDICAL_LICENSE` and `US_DRIVER_LICENSE`.

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/license.py` — `CertificateLicenseRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/license.py:69` — `supported_entity="CERTIFICATE_LICENSE_NUMBER"` (4 patterns: DEA, NPI, alphanumeric, numeric)
- `src/scanmenow/detection/recognizers/__init__.py:34` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:148` — `_find(..., "CERTIFICATE_LICENSE_NUMBER")` positive assertion
- `tests/test_hipaa_recognizers.py:155` — `_find(..., "CERTIFICATE_LICENSE_NUMBER")` negative assertion

**Status:** ✓ implemented and tested (Task #3)

---

## `VEHICLE_IDENTIFIER`

Vehicle Identification Number (VIN) — 17-character NHTSA format (excludes I/O/Q per NHTSA spec); also covers US license plate patterns.

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/vehicle.py` — `VehicleIdentifierRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/vehicle.py:48` — `supported_entity="VEHICLE_IDENTIFIER"` (2 patterns: VIN, license plate)
- `src/scanmenow/detection/recognizers/__init__.py:35` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:86` — `_find(..., "VEHICLE_IDENTIFIER")` positive assertion
- `tests/test_hipaa_recognizers.py:93` — `_find(..., "VEHICLE_IDENTIFIER")` negative assertion
- `tests/test_hipaa_recognizers.py:228` — counted in multi-entity integration test

**Status:** ✓ implemented and tested (Task #3)

---

## `DEVICE_IDENTIFIER`

Device identifier or serial number — alphanumeric serial patterns with context keywords ("serial", "device ID", "S/N", "serial number"). Recall-biased; high variability across manufacturers.

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/device.py` — `DeviceIdentifierRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/device.py:68` — `supported_entity="DEVICE_IDENTIFIER"` (4 patterns: SN prefix, UDI, alphanumeric, numeric)
- `src/scanmenow/detection/recognizers/__init__.py:36` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:167` — `_find(..., "DEVICE_IDENTIFIER")` positive assertion
- `tests/test_hipaa_recognizers.py:174` — `_find(..., "DEVICE_IDENTIFIER")` negative assertion

**Status:** ✓ implemented and tested (Task #3)

---

## `BIOMETRIC_IDENTIFIER`

Biometric identifier — text-description patterns ("fingerprint", "voiceprint", "retina scan", "iris scan"). Best-effort only; high false-negative rate for non-descriptive references. Documented limitation: do not apply accuracy thresholds to this identifier.

**Source:** Custom `PatternRecognizer` — implemented in Task #3
**Recognizer:** `src/scanmenow/detection/recognizers/biometric.py` — `BiometricIdentifierRecognizer`

**Producers**
- `src/scanmenow/detection/recognizers/biometric.py:78` — `supported_entity="BIOMETRIC_IDENTIFIER"` (7 keyword patterns)
- `src/scanmenow/detection/recognizers/__init__.py:37` — included in `ALL_RECOGNIZERS`
- `src/scanmenow/detection/analyzer.py:14` — registered via `build_analyzer()` loop

**Consumers**
- `tests/test_hipaa_recognizers.py:186` — `_find(..., "BIOMETRIC_IDENTIFIER")` positive assertion
- `tests/test_hipaa_recognizers.py:193` — `_find(..., "BIOMETRIC_IDENTIFIER")` negative assertion

**Status:** ✓ implemented and tested (Task #3) — documented best-effort limitation in `docs/hipaa_coverage.json`

---

## Out-of-Scope HIPAA Safe Harbor Identifiers

| Identifier | Reason |
|------------|--------|
| Full-face photographs | Not applicable to text scanning |

---

## Summary

| Entity Type | Source | Consumers | Status |
|-------------|--------|-----------|--------|
| `EMAIL_ADDRESS` | Native | test_detection.py, test_storage.py | ✓ native |
| `PERSON` | Native (spaCy) | test_detection.py, test_storage.py | ✓ native |
| `PHONE_NUMBER` | Native | (none yet) | ✓ native — HIPAA coverage confirmed |
| `US_SSN` | Native | (none yet) | ✓ native — HIPAA coverage confirmed |
| `IP_ADDRESS` | Native | (none yet) | ✓ native — HIPAA coverage confirmed |
| `URL` | Native | (none yet) | ✓ native — HIPAA coverage confirmed |
| `LOCATION` | Native (spaCy) | (none yet) | ✓ native — HIPAA coverage confirmed |
| `DATE_TIME` | Native | (none yet) | ✓ native — HIPAA coverage confirmed |
| `MEDICAL_RECORD_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `HEALTH_PLAN_BENEFICIARY` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `ACCOUNT_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `CERTIFICATE_LICENSE_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `VEHICLE_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `DEVICE_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented and tested |
| `BIOMETRIC_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ✓ implemented (best-effort) |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-25T01:00:00Z (by /cross-boundary-audit — Task #3 post-build verification)

**Boundaries checked:** Presidio entity type strings (full code scan — all recognizer modules, __init__, analyzer, tests)

**Evidence recorded:**
- 9 entries with complete producer/consumer pairs ✓ (`EMAIL_ADDRESS`, `PERSON` — smoke-tested; `MEDICAL_RECORD_NUMBER`, `HEALTH_PLAN_BENEFICIARY`, `ACCOUNT_NUMBER`, `CERTIFICATE_LICENSE_NUMBER`, `VEHICLE_IDENTIFIER`, `DEVICE_IDENTIFIER`, `BIOMETRIC_IDENTIFIER` — Task #3 built and passing)
- 6 entries confirmed native with no bespoke test consumers ✓ (`PHONE_NUMBER`, `US_SSN`, `IP_ADDRESS`, `URL`, `LOCATION`, `DATE_TIME`)
- 0 planned entries ⚠ — all 7 Task #3 custom types now implemented
- New identifiers introduced on Task #3 (shipped): `MEDICAL_RECORD_NUMBER`, `HEALTH_PLAN_BENEFICIARY`, `ACCOUNT_NUMBER`, `CERTIFICATE_LICENSE_NUMBER`, `VEHICLE_IDENTIFIER`, `DEVICE_IDENTIFIER`, `BIOMETRIC_IDENTIFIER`
- Registries match current code diff: ✓ (all 7 custom recognizers present in `src/scanmenow/detection/recognizers/`, registered in `build_analyzer()`, tested in `tests/test_hipaa_recognizers.py` — 27/27 tests passing)

**Gaps identified:** none

**Status:** ✓ Audit complete (Task #3 post-build)
