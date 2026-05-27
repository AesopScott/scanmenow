# ScanMeNow — Group C Corpus Specification
## Synthetic PHI Corpus & Golden Findings

**Version:** 1.0  
**Issued:** 2026-05-27  
**Purpose:** Requirements for an independent party to build the synthetic PHI test corpus that validates, benchmarks, and regression-guards the ScanMeNow detection engine.

---

## What You Are Being Asked to Build

ScanMeNow is a text-scanning tool that detects Protected Health Information (PHI) in documents. The engineering team has built and internally tested the detection engine. You are being asked to produce an **independent test corpus** — a set of realistic-looking synthetic documents containing known PHI, paired with a ground-truth JSON file that records exactly what PHI is in each document and where.

This corpus will be used to:

1. **Validate** that the detection engine finds PHI it is supposed to find on data the engineers did not hand-craft for their own tests.
2. **Benchmark** accuracy per identifier type — how often does the engine catch what it should catch?
3. **Regression-guard** — if a future code change silently breaks detection, the test suite catches it.

**Critical independence constraint:** Do not look at, read, or consult the ScanMeNow source code, its test files, or any existing test fixtures when writing this corpus. The value of your contribution is that it is genuinely independent. Documents you write based on knowledge of the implementation will not catch real-world failures.

---

## Identifiers to Cover

Your corpus must exercise all **15 unique detectable entity labels** below. These map to the HIPAA Safe Harbor de-identification standard. Note that HIPAA identifiers #4 (phone) and #5 (fax) share a single label — `PHONE_NUMBER` — because fax numbers are structurally identical to phone numbers. There are 16 HIPAA rows but 15 distinct labels.

| HIPAA # | Identifier Type | **Label (use exactly)** | Realistic Example Format | Notes |
|---|---|---|---|---|
| 1 | Full name | `PERSON` | "Jane Doe", "Dr. Marcus Webb" | First+last, or titled name |
| 2 | Geographic data smaller than state | `LOCATION` | "742 Evergreen Terrace, Springfield", "ZIP 60601" | Street address, city, zip, county |
| 3 | Date (except year alone) | `DATE_TIME` | "March 14, 2019", "03/14/2019", "2019-03-14" | Birth dates, admission dates, discharge dates |
| 4 & 5 | Phone **and** fax numbers | `PHONE_NUMBER` | "(312) 555-0198"; "Fax: 312-555-0122" | Same label for both. Include at least 1 fax instance with the word "fax" nearby |
| 6 | Email address | `EMAIL_ADDRESS` | "jdoe@hospital.org" | Standard email |
| 7 | Social Security Number | `US_SSN` | "SSN: 312-56-7890" | NNN-NN-NNNN format |
| 8 | Medical record number | `MEDICAL_RECORD_NUMBER` | "MRN: 7834291", "Medical Record: MR-0042871" | Typically 6–10 digits, often prefixed |
| 9 | Health plan beneficiary number | `HEALTH_PLAN_BENEFICIARY` | "Member ID: XJ7291003", "Beneficiary: BC-4482910" | Alphanumeric, often prefixed |
| 10 | Account number | `ACCOUNT_NUMBER` | "Account #: 4829100372", "Acct: 77-839-2201" | Billing account, utility, retail |
| 11 | Certificate or license number | `CERTIFICATE_LICENSE_NUMBER` | "License #: A1289374", "DEA: AB1234563" | Professional license, DEA number, certificate |
| 12 | Vehicle identifier (VIN or plate) | `VEHICLE_IDENTIFIER` | "VIN: 1HGBH41JXMN109186", "Plate: 7ABC234" | 17-char VIN or US license plate |
| 13 | Device identifier or serial number | `DEVICE_IDENTIFIER` | "S/N: SN-28847291", "Device ID: DVC-0029183" | Medical device, implant, serial number |
| 14 | Web URL | `URL` | "https://patient.hospital.org/records/4829" | Any http/https URL |
| 15 | IP address | `IP_ADDRESS` | "192.168.10.44", "2001:0db8::1" | IPv4 or IPv6 |
| 16 | Biometric identifier | `BIOMETRIC_IDENTIFIER` | "patient's fingerprint", "voiceprint on file" | Text description only; best-effort |

**Note on #16 (Biometric):** This tool detects text *descriptions* of biometric data (e.g., "fingerprint record"), not actual biometric data. Include 2–3 natural-language mentions across the corpus. No accuracy threshold will be applied to this type.

**Out of scope — do not include:** HIPAA #17 (full-face photographs) is not applicable to text scanning. HIPAA #18 (any other unique identifying number) is a catch-all clause not directly detectable as a discrete entity type. Neither appears in the engine's label set and neither should appear in `golden_findings.json`.

---

## Document Requirements

### Quantity

Produce a minimum of **15 documents** — enough to cover all required formats. Suggested distribution:

| Document Type | Suggested Format | Count |
|---|---|---|
| Patient intake / registration form (native) | `.docx` | 1 |
| Patient intake / registration form (scanned image) | `.png` or `.jpg` | 1 |
| Clinical note / discharge summary | `.docx` | 1 |
| Clinical note (photographed / scanned) | `.jpg` or `.tiff` | 1 |
| Insurance claim / explanation of benefits (text PDF) | `.pdf` (text layer) | 1 |
| Insurance claim (scanned PDF) | `.pdf` (image-only) | 1 |
| Lab report | `.txt` | 1 |
| Lab result (scanned) | `.tiff` | 1 |
| Medical device incident report | `.doc` (legacy) | 1 |
| HR / employee health record | `.xls` (legacy) | 1 |
| Case summary presentation | `.pptx` | 1 |
| Patient register export | `.csv` | 1 |
| Consent form (scanned) | `.bmp` | 1 |
| Billing ledger | `.xlsx` | 1 |
| Free-form mixed-content (all identifier types) | `.txt` | 1 |

### Coverage requirement

Across the full corpus, every identifier type in the table above must appear **at least 3 times** in at least **2 different documents**. More is better. Do not cluster all instances of one type into a single document.

### Realism

Documents must look like plausible real-world healthcare or administrative records. They should not look like a list of test cases or a table of examples. Use natural prose, plausible fictional names, realistic institutional names (hospitals, insurance companies, employers), and correct contextual framing (e.g., a VIN appears in a vehicle accident report, not a clinical note).

All PHI must be **synthetic and fictional** — do not use real names, real SSNs, real addresses, or any real person's data.

### Format variety

Use a mix of formats within documents:
- Phone numbers in multiple formats: `(312) 555-0198`, `312-555-0198`, `312.555.0198`, `+1-312-555-0198`
- Dates in multiple formats: `March 14, 2019`, `03/14/2019`, `2019-03-14`, `14 March 2019`
- MRNs with different prefixes: `MRN: 7834291`, `Medical Record #: 7834291`, `MR-7834291`, bare `7834291` with "medical record" nearby
- Account numbers with different delimiters and widths: `4829100372`, `77-839-2201`, `ACC-00291834`

This variety is essential. If all instances of a type are in the same format, a broken recognizer that only handles one format would appear to work correctly.

### Near-miss decoys (required)

Each document must include **at least 2 near-miss values** — numbers or patterns that resemble PHI but are not:
- Invoice numbers that look like account numbers: `Invoice #: 9182734`
- Reference codes that look like MRNs: `Ref: 8374921`
- Dates that are years only (not HIPAA-covered): `built in 2018`
- Random 17-character product codes that are not VINs
- Plain IP-looking strings: `version 10.2.1` (not a real IP)

Near-miss decoys allow the benchmark to measure **false positives** — identifiers the engine flags that it shouldn't.

---

## Output Files

Produce two things:

### 1. Document files

One file per document. Use the format most natural for that document type. Supported formats:

**Text-native formats** (text extracted directly — no OCR required):

| Extension | Format | Notes |
|---|---|---|
| `.txt` | Plain UTF-8 text | Simplest; use for free-form notes and logs |
| `.csv` | Comma-separated values | Use for tabular data — patient registers, exported billing |
| `.docx` | Word (Open XML) | Use for clinical notes, letters, intake forms |
| `.doc` | Word (legacy binary) | Fully supported via LibreOffice headless (system install required — see below). Include at least 1 document. |
| `.xlsx` | Excel (Open XML) | Use for billing records, patient lists |
| `.xls` | Excel (legacy binary) | Include at least 1 legacy format document. Extracted via `xlrd` (read-only, no formula evaluation). |
| `.pptx` | PowerPoint (Open XML) | Use for case summary slide decks |
| `.pdf` | PDF (text-layer present) | Use for forms, reports, EOBs — must have a selectable text layer |

**Image formats** (OCR required — text extracted via the OCR engine added in Task D):

| Extension | Format | Notes |
|---|---|---|
| `.png` | PNG image | Use for scanned forms, screenshots of records |
| `.jpg` / `.jpeg` | JPEG image | Use for photographed documents, scanned pages |
| `.tiff` / `.tif` | TIFF image | Use for high-resolution scans; common in medical imaging systems |
| `.bmp` | BMP image | Use for at least 1 document; tests uncompressed format handling |
| `.pdf` (image-only) | Scanned PDF (no text layer) | Use for at least 1 document; all content is rasterized |

> **Note on scanned PDF:** Include both a text-layer PDF (listed above under text-native) and an image-only scanned PDF. Use clearly distinct filenames so the format is unambiguous, e.g., `doc_011_eob_text.pdf` vs. `doc_012_referral_scanned.pdf`.

```
corpus/
  doc_001_patient_intake.docx            ← text-native; companion .extracted.txt required
  doc_002_discharge_summary.docx         ← text-native; companion .extracted.txt required
  doc_003_insurance_claim_eob.pdf        ← text-layer PDF; companion .extracted.txt required
  doc_004_lab_report.txt                 ← plain text; no companion needed
  doc_005_device_incident.doc            ← legacy binary; best-effort extraction
  doc_006_employee_health.xls            ← legacy Excel; companion .extracted.txt required
  doc_007_case_summary.pptx             ← text-native; companion .extracted.txt required
  doc_008_patient_register.csv           ← plain text; no companion needed
  doc_009_billing_ledger.xlsx            ← text-native; companion .extracted.txt required
  doc_010_mixed_content.txt              ← plain text; no companion needed
  doc_011_intake_scan.png                ← OCR required; companion .extracted.txt required
  doc_012_referral_scan.jpg              ← OCR required; companion .extracted.txt required
  doc_013_lab_result_scan.tiff           ← OCR required; companion .extracted.txt required
  doc_014_consent_form_scan.bmp          ← OCR required; companion .extracted.txt required
  doc_015_insurance_claim_scanned.pdf    ← image-only PDF / OCR; companion .extracted.txt required
  ...
```

Use realistic file names. At least **one document in each of these formats** must be present: `.txt`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.pptx`, `.csv`, `.pdf` (text-layer), `.png`, `.jpg`, `.tiff`, `.bmp`, `.pdf` (image-only/scanned).

**Important — companion extracted text files:**

All `start`/`end` offsets in `golden_findings.json` must refer to character positions in the **extracted plain text** of the document — not raw bytes, binary content, or pixel data. For every document that is not already plain `.txt` or `.csv`, provide a companion `.extracted.txt` file:

```
corpus/
  doc_001_patient_intake.docx
  doc_001_patient_intake.extracted.txt   ← text extracted by python-docx

  doc_011_intake_scan.png
  doc_011_intake_scan.extracted.txt      ← text extracted by OCR engine
```

**For Office and text-layer PDF files:** Use the extraction library listed below and document the exact tool version in your delivery notes:

| Format | Library / tool | Notes |
|---|---|---|
| `.docx` | `python-docx` | Iterates paragraphs and table cells; joins with `\n` |
| `.doc` | LibreOffice headless | Convert to `.txt` via subprocess (see command below); requires LibreOffice system install |
| `.xlsx` | `openpyxl` | Reads cell values row by row across all sheets |
| `.xls` | `xlrd` | Read-only; same row-by-row approach |
| `.pptx` | `python-pptx` | Reads text frames across all slides |
| `.pdf` (text layer) | `pdfplumber` | Extracts text page by page; concatenate with `\n` |

**`.doc` extraction command (use exactly):**

```python
import subprocess, pathlib, tempfile, shutil

def extract_doc(doc_path: str) -> str:
    """Extract plain text from a legacy .doc file via LibreOffice headless."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            ["soffice", "--headless", "--convert-to", "txt:Text",
             "--outdir", tmp, doc_path],
            check=True, capture_output=True,
        )
        stem = pathlib.Path(doc_path).stem
        txt_path = pathlib.Path(tmp) / f"{stem}.txt"
        return txt_path.read_text(encoding="utf-8", errors="replace")
```

Run LibreOffice version `≥ 7.4`. Document the exact version used in your delivery notes — LibreOffice's `.doc` text extraction is deterministic across patch releases within a minor version but may vary across minor versions.

**For image files and scanned PDFs:** The extraction must use the same OCR engine that ScanMeNow Task D will use — **Tesseract via `pytesseract`**, English language pack (`eng`), default PSM. Run OCR exactly as follows so offsets match what the benchmark will produce:

```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open("doc_011_intake_scan.png"), lang="eng")
with open("doc_011_intake_scan.extracted.txt", "w", encoding="utf-8") as f:
    f.write(text)
```

For scanned PDFs, convert pages to images first (300 DPI recommended), OCR each page, then concatenate with a single newline between pages.

The benchmark engine will replicate this extraction exactly. If you use a different OCR config, offsets will not match. If your OCR output and the benchmark's OCR output differ by even one character, every subsequent offset will be wrong — verify with the offset check script below.

### 2. Golden findings file — `golden_findings.json`

One JSON file documenting every PHI instance in the corpus. This is the ground truth the benchmark engine will compare against.

**Schema:**

```json
{
  "corpus_version": "1.0",
  "produced_by": "<your name or org>",
  "produced_at": "<ISO 8601 date>",
  "documents": [
    {
      "doc_id": "doc_001",
      "filename": "doc_001_patient_intake.txt",
      "description": "Patient intake form — Jane Doe, admitted March 14 2019",
      "findings": [
        {
          "id": "doc_001_f001",
          "entity_type": "PERSON",
          "start": 42,
          "end": 50,
          "text": "Jane Doe",
          "context": "Patient name: Jane Doe, DOB:",
          "notes": "Patient full name, first occurrence"
        },
        {
          "id": "doc_001_f002",
          "entity_type": "DATE_TIME",
          "start": 96,
          "end": 109,
          "text": "March 14, 2019",
          "context": "DOB: March 14, 2019. Admitted",
          "notes": "Date of birth"
        }
      ],
      "decoys": [
        {
          "id": "doc_001_d001",
          "text": "Invoice #: 9182734",
          "start": 310,
          "end": 328,
          "intended_type": "none",
          "resembles": "ACCOUNT_NUMBER",
          "notes": "Invoice number — should NOT be flagged as an account number"
        }
      ]
    }
  ]
}
```

**Field definitions:**

| Field | Type | Required | Description |
|---|---|---|---|
| `doc_id` | string | ✓ | Unique document identifier, matches filename prefix |
| `filename` | string | ✓ | Exact filename in the `corpus/` directory |
| `findings[].id` | string | ✓ | Unique finding ID within the corpus, format `{doc_id}_f{NNN}` |
| `findings[].entity_type` | string | ✓ | **Must be exactly one of the labels in the identifier table above** |
| `findings[].start` | integer | ✓ | Zero-based character offset of the first character of the PHI value |
| `findings[].end` | integer | ✓ | Zero-based character offset of the character *after* the last character (Python slice convention: `text[start:end]`) |
| `findings[].text` | string | ✓ | The exact PHI string — must match `document_text[start:end]` exactly |
| `findings[].context` | string | ✓ | ~30-char window around the finding for human readability |
| `findings[].notes` | string | ✗ | Optional human note (e.g., "date of birth", "second occurrence") |
| `decoys[].id` | string | ✓ | Unique decoy ID, format `{doc_id}_d{NNN}` |
| `decoys[].text` | string | ✓ | The exact decoy string |
| `decoys[].start` / `.end` | integer | ✓ | Character offsets, same convention as findings |
| `decoys[].intended_type` | string | ✓ | Always `"none"` — this is not PHI |
| `decoys[].resembles` | string | ✓ | Which entity type it resembles (so the benchmark can measure false positives by type) |

### Offset verification

Before delivering, verify your offsets are correct by running this check against each document:

```python
import json, pathlib

# For plain .txt and .csv: read the document directly.
# For all other formats: read the companion .extracted.txt file.
# Example for a .docx document:
doc_text = pathlib.Path("corpus/doc_001_patient_intake.extracted.txt").read_text(encoding="utf-8")

findings = [...]  # load from golden_findings.json for this document

for f in findings:
    extracted = doc_text[f["start"]:f["end"]]
    assert extracted == f["text"], (
        f"Offset mismatch for {f['id']}: "
        f"expected '{f['text']}', got '{extracted}'"
    )
print("All offsets verified.")
```

Run this for every document — using the raw `.txt`/`.csv` file directly, and the `.extracted.txt` companion for everything else. This check must pass for every finding and every decoy before delivery.

---

## Accuracy Thresholds

The benchmark will compare the engine's output against your golden findings and compute:

- **Recall** (per type): fraction of golden findings the engine detected
- **Precision** (per type): fraction of engine findings that were in the golden set (or near-miss decoys)
- **False positive rate** (per type): decoys the engine incorrectly flagged

The following thresholds define a passing build. Do not adjust your corpus to hit these thresholds — write realistic documents and let the numbers fall where they do.

| Identifier Type | Minimum Recall | Notes |
|---|---|---|
| `EMAIL_ADDRESS` | 90% | High-precision format |
| `US_SSN` | 90% | High-precision format |
| `PERSON` | 75% | NER-based; may miss initials, nicknames |
| `LOCATION` | 70% | NER-based; may miss bare zip codes |
| `DATE_TIME` | 80% | Multi-format; year-only not counted |
| `PHONE_NUMBER` | 80% | Covers fax (same type) |
| `IP_ADDRESS` | 90% | High-precision format |
| `URL` | 90% | High-precision format |
| `MEDICAL_RECORD_NUMBER` | 65% | Context-anchored; recall-biased |
| `HEALTH_PLAN_BENEFICIARY` | 65% | Context-anchored; recall-biased |
| `ACCOUNT_NUMBER` | 60% | High false-positive tolerance |
| `CERTIFICATE_LICENSE_NUMBER` | 60% | High false-positive tolerance |
| `VEHICLE_IDENTIFIER` | 75% | VIN format well-defined; plates variable |
| `DEVICE_IDENTIFIER` | 60% | High format variability |
| `BIOMETRIC_IDENTIFIER` | no threshold | Best-effort keyword detection only |

---

## How Your Corpus Will Be Used — Benchmark Runner Architecture

This section describes how the engineering team will consume the corpus you produce. Understanding this helps you write documents and offsets that will work correctly.

### Three-layer architecture

```
src/scanmenow/benchmark/
  runner.py      ← core logic: loads corpus, runs analyzer, computes metrics
  report.py      ← formats results as terminal table or JSON file

tests/
  test_benchmark.py   ← pytest wrapper: skips if corpus not present,
                         asserts thresholds when it is

CLI:
  scanmenow benchmark --corpus ./corpus [--output report.json]
```

**`runner.py`** is the engine. For each document in `golden_findings.json` it:
1. Extracts plain text from the source file using the same extraction stack described in this spec (python-docx for `.docx`, LibreOffice headless for `.doc`, pytesseract for images, etc.)
2. Runs `build_analyzer()` on the extracted text
3. Compares the analyzer's output spans against your golden `findings[]`, allowing a configurable character-offset tolerance for OCR-derived documents (default ±5 chars)
4. Records true positives, false negatives, and false positives (matched against `decoys[]`)
5. Returns a `BenchmarkResult` dataclass with per-type recall, precision, and false-positive rate

**`tests/test_benchmark.py`** calls the runner and fails CI if any required entity type falls below its threshold. It uses `pytest.mark.skipif` — if the `corpus/` directory is not present, the test silently skips rather than erroring. This means normal development runs are unaffected; the benchmark only gates CI once the corpus is delivered and placed in the expected path.

**`scanmenow benchmark --corpus ./corpus`** calls the same runner and prints a formatted table to the terminal:

```
Entity Type                   Recall    Precision   FP Rate   Threshold   Status
─────────────────────────────────────────────────────────────────────────────────
EMAIL_ADDRESS                  97%        99%         1%         90%       ✓ PASS
US_SSN                         94%        100%        0%         90%       ✓ PASS
PERSON                         71%        83%         9%         75%       ✗ FAIL
MEDICAL_RECORD_NUMBER          68%        61%        22%         65%       ✓ PASS
BIOMETRIC_IDENTIFIER           38%        n/a         n/a        none      ~ (no threshold)
─────────────────────────────────────────────────────────────────────────────────
Result: 1 type below threshold (PERSON)
```

This CLI command is also what you should run against your corpus **before delivery** to verify your offsets and coverage produce sensible results. You can install the tool locally with `uv pip install -e .` in the project directory (requires Python ≥ 3.11 and uv).

### Offset matching

For text-native formats (`.txt`, `.csv`, `.docx`, `.xlsx`, `.pptx`, `.pdf` text-layer, `.doc`), the benchmark matches exact character offsets — `text[start:end]` must equal `findings[].text` exactly.

For OCR-derived formats (`.png`, `.jpg`, `.tiff`, `.bmp`, `.pdf` image-only), the benchmark applies a **±5 character tolerance** on span boundaries. OCR output is deterministic given the same engine and config, but whitespace normalisation can shift offsets by a few characters. This tolerance is why the spec requires you to produce `.extracted.txt` companions using exactly the Tesseract configuration described above — if you use a different config, even the ±5 tolerance may not save you.

### What "false positive" means in the benchmark

A false positive is an engine finding that does **not** match any entry in `findings[]` or `decoys[]` for that document. Decoys let you distinguish between:

- **Intentional near-miss:** the engine flagged a decoy — expected noise, counted separately
- **Unexpected false positive:** the engine flagged something that isn't in either list — uncontrolled noise

This is why the near-miss decoy requirement exists: without `decoys[]`, every unexpected engine hit looks the same as a known near-miss, and precision measurements are meaningless.

---

## Delivery Checklist

Before submitting the corpus:

- [ ] At least 15 documents in `corpus/` covering all required formats
- [ ] At least one document in each of: `.txt`, `.csv`, `.docx`, `.doc`, `.xlsx`, `.xls`, `.pptx`, `.pdf` (text-layer), `.png`, `.jpg`, `.tiff`, `.bmp`, `.pdf` (image-only/scanned)
- [ ] Every non-plaintext document has a companion `.extracted.txt` file
- [ ] Office and text-PDF extractions use the specified libraries: `python-docx` (`.docx`), LibreOffice headless ≥ 7.4 (`.doc`), `xlrd` (`.xls`), `openpyxl` (`.xlsx`), `python-pptx` (`.pptx`), `pdfplumber` (`.pdf` text-layer)
- [ ] Image and scanned-PDF extractions use **Tesseract via pytesseract**, `lang="eng"`, default PSM, exactly as shown in the spec
- [ ] Extraction tool, version, and exact command documented in delivery notes for every format
- [ ] Every identifier type appears in ≥ 3 findings across ≥ 2 documents
- [ ] Image-format documents include PHI that is clearly legible (high contrast, ≥ 150 DPI, unobscured)
- [ ] At least 2 near-miss decoys per document, each recorded in `decoys[]`
- [ ] All PHI format variants covered across the corpus (see "Format variety" section)
- [ ] Offset verification script passes for all documents (run against `.extracted.txt` for all non-plaintext files)
- [ ] `golden_findings.json` is valid JSON with no missing required fields
- [ ] `entity_type` values use **exactly** the labels in the identifier table — no variations, no lowercase, no spaces
- [ ] No real personal data used anywhere

---

## Questions

If anything in this spec is ambiguous, ask before writing documents — offset errors found after writing are expensive to fix. The most common mistake is off-by-one errors in character offsets; use the verification script continuously as you write.

Contact: ravenshroud@gmail.com
