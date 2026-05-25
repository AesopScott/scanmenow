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

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/mrn.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/mrn.py` — `MedicalRecordRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.1

---

## `HEALTH_PLAN_BENEFICIARY`

Health plan beneficiary number / member ID — health plan ID patterns with context keywords ("beneficiary", "member ID", "plan ID").

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/beneficiary.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/beneficiary.py` — `HealthPlanBeneficiaryRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.1

---

## `ACCOUNT_NUMBER`

Generic financial account number — numeric patterns with context keywords ("account", "acct", "account number"). Recall-biased; some false positives acceptable.

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/account.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/account.py` — `AccountNumberRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.2

---

## `CERTIFICATE_LICENSE_NUMBER`

Certificate or license number — alphanumeric patterns with context keywords ("license", "certificate", "cert", "credential"). Recall-biased.

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/license.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/license.py` — `CertificateLicenseRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.2

---

## `VEHICLE_IDENTIFIER`

Vehicle Identification Number (VIN) — 17-character NHTSA format with strict checksum-compatible regex; also covers license plate patterns.

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/vehicle.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/vehicle.py` — `VehicleIdentifierRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.1

---

## `DEVICE_IDENTIFIER`

Device identifier or serial number — alphanumeric serial patterns with context keywords ("serial", "device ID", "S/N", "serial number"). Recall-biased.

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/device.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/device.py` — `DeviceIdentifierRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.2

---

## `BIOMETRIC_IDENTIFIER`

Biometric identifier — text-description patterns ("fingerprint", "voiceprint", "retina scan", "iris scan"). Best-effort only; high false-negative rate expected for non-descriptive biometric references.

**Source:** Custom `PatternRecognizer` — **planned in Task #3**
**Recognizer:** `src/scanmenow/detection/recognizers/biometric.py` *(not yet created)*

**Producers**
- `src/scanmenow/detection/recognizers/biometric.py` — `BiometricIdentifierRecognizer` *(planned)*

**Consumers**
- `tests/test_hipaa_recognizers.py` — positive/negative unit tests *(planned)*

**Status:** ⚠ planned — Task #3, Phase 2, Task 2.2 (best-effort; documented limitation in hipaa_coverage.json)

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
| `MEDICAL_RECORD_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `HEALTH_PLAN_BENEFICIARY` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `ACCOUNT_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `CERTIFICATE_LICENSE_NUMBER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `VEHICLE_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `DEVICE_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |
| `BIOMETRIC_IDENTIFIER` | Custom (Task #3) | test_hipaa_recognizers.py | ⚠ planned |

---

## Audit Trail — Proof of Registry Verification

**Last audit:** 2026-05-25T00:00:00Z (by /cross-boundary-audit — pre-build plan validation for Task #3)

**Boundaries checked:** Presidio entity type strings (code scan + Task #3 plan review)

**Evidence recorded:**
- 2 entries with complete producer/consumer pairs ✓ (`EMAIL_ADDRESS`, `PERSON` — smoke-tested)
- 6 entries confirmed native with no test consumers yet ✓ (HIPAA coverage audit)
- 7 entries planned ⚠ (Task #3 custom recognizers — not yet built)
- New identifiers introduced on task #3 (planned): `MEDICAL_RECORD_NUMBER`, `HEALTH_PLAN_BENEFICIARY`, `ACCOUNT_NUMBER`, `CERTIFICATE_LICENSE_NUMBER`, `VEHICLE_IDENTIFIER`, `DEVICE_IDENTIFIER`, `BIOMETRIC_IDENTIFIER`
- Registries match current code diff: ✓ (no Task #3 code exists yet — registry pre-declares planned types)

**Gaps identified:**
- 7 custom entity types planned but not yet implemented (Task #3 build will resolve these)

**Status:** ✓ Audit complete (pre-build plan validation)
