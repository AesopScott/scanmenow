"""
Custom PatternRecognizer sub-package for HIPAA Safe Harbor identifiers.

Exports ALL_RECOGNIZERS — a list of instantiated recognizer objects
covering the 7 HIPAA Safe Harbor identifiers not natively detected by
Presidio. Register these with AnalyzerEngine.registry.add_recognizer().

Entity types introduced by this package:
  MEDICAL_RECORD_NUMBER     — HIPAA #8
  HEALTH_PLAN_BENEFICIARY   — HIPAA #9
  ACCOUNT_NUMBER            — HIPAA #10 (supplemental)
  CERTIFICATE_LICENSE_NUMBER — HIPAA #11 (supplemental)
  VEHICLE_IDENTIFIER        — HIPAA #12
  DEVICE_IDENTIFIER         — HIPAA #13
  BIOMETRIC_IDENTIFIER      — HIPAA #16
"""

from .account import AccountNumberRecognizer
from .beneficiary import HealthPlanBeneficiaryRecognizer
from .biometric import BiometricIdentifierRecognizer
from .device import DeviceIdentifierRecognizer
from .license import CertificateLicenseRecognizer
from .mrn import MedicalRecordRecognizer
from .vehicle import VehicleIdentifierRecognizer

ALL_RECOGNIZERS = [
    MedicalRecordRecognizer(),
    HealthPlanBeneficiaryRecognizer(),
    AccountNumberRecognizer(),
    CertificateLicenseRecognizer(),
    VehicleIdentifierRecognizer(),
    DeviceIdentifierRecognizer(),
    BiometricIdentifierRecognizer(),
]

__all__ = [
    "MedicalRecordRecognizer",
    "HealthPlanBeneficiaryRecognizer",
    "AccountNumberRecognizer",
    "CertificateLicenseRecognizer",
    "VehicleIdentifierRecognizer",
    "DeviceIdentifierRecognizer",
    "BiometricIdentifierRecognizer",
    "ALL_RECOGNIZERS",
]
