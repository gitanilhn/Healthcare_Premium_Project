import os
from pathlib import Path


# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ==========================================================
# MODEL CONFIGURATION
# ==========================================================

MODEL_SOURCE = os.getenv(
    "MODEL_SOURCE",
    "local",
).strip().lower()


MODEL_BUCKET = os.getenv(
    "MODEL_BUCKET",
    "healthcare-premium-mlops-anil",
)


MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "models/healthcare-premium-prediction/v1",
)


MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "v1",
)


AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-1",
)


# ==========================================================
# LOCAL ARTIFACT DIRECTORY
# ==========================================================

# Local development:
#
# G:\MLOPS_ANIL\Healthcare_Premium_Prediction\
#     artifacts\
#         latest\
#
# Kubernetes:
#
# /app/artifacts/latest
#
# The ARTIFACT_DIR environment variable can override
# the default location.

DEFAULT_ARTIFACT_DIR = (
    PROJECT_ROOT
    / "artifacts"
    / "latest"
)


ARTIFACT_DIR = Path(
    os.getenv(
        "ARTIFACT_DIR",
        str(DEFAULT_ARTIFACT_DIR),
    )
)


# ==========================================================
# ARTIFACT FILE NAMES
# ==========================================================

MODEL_FILE = "model.pkl"

PREPROCESSOR_FILE = "preprocessor.pkl"

METADATA_FILE = "metadata.json"

FEATURE_SCHEMA_FILE = "feature_schema.json"


# ==========================================================
# LOGGING / CONFIGURATION DISPLAY
# ==========================================================

print("=" * 70)
print("MODEL CONFIGURATION")
print("=" * 70)

print(
    f"MODEL_SOURCE       : {MODEL_SOURCE}"
)

print(
    f"MODEL_BUCKET       : {MODEL_BUCKET}"
)

print(
    f"MODEL_PREFIX       : {MODEL_PATH}"
)

print(
    f"MODEL_VERSION      : {MODEL_VERSION}"
)

print(
    f"AWS_REGION         : {AWS_REGION}"
)

print(
    f"ARTIFACT_DIRECTORY : {ARTIFACT_DIR}"
)

print(
    f"MODEL_FILE         : {MODEL_FILE}"
)

print(
    f"PREPROCESSOR_FILE  : {PREPROCESSOR_FILE}"
)

print(
    f"METADATA_FILE      : {METADATA_FILE}"
)

print(
    f"FEATURE_SCHEMA_FILE: {FEATURE_SCHEMA_FILE}"
)

print("=" * 70)