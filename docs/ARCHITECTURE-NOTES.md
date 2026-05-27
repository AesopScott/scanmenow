# ScanMeNow Architecture Notes

## Phase 1 Task Dependency Map

Task C is the benchmark and accuracy gate. It depends on three upstream workstreams:

- **Task D - Filesystem Walker & Integration:** provides file discovery plus text extraction/OCR for Office, PDF, image, and scanned-PDF formats.
- **Task G - PII Scope and Capability:** expands detection beyond PHI so the benchmark covers the final PHI/PII entity set.
- **Task H - Independent Testing Data for Task C:** produces the independent synthetic testing corpus, companion extracted text files, golden findings, decoys, and delivery notes.

Task C consumes D, G, and H to run repeatable accuracy checks, compute per-entity recall/precision, and regression-guard the scanner without relying on engineer-authored fixtures.
