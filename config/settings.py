import os
from pathlib import Path


# ============================================================
# AWS CONFIGURATION
# ============================================================

AWS_REGION = os.getenv(
    "AWS_REGION",
    os.getenv(
        "AWS_DEFAULT_REGION",
        "ap-south-1",
    ),
)


# ============================================================
# MODEL CONFIGURATION
# ============================================================

# Model source:
#
# local
#     Load model artifacts from local artifacts directory.
#
# s3
#     Load model artifacts from Amazon S3.
#
MODEL_SOURCE = os.getenv(
    "MODEL_SOURCE",
    "local",
).lower()


# ============================================================
# S3 MODEL CONFIGURATION
# ============================================================

MODEL_BUCKET = os.getenv(
    "MODEL_BUCKET",
    "healthcare-premium-mlops-anil",
)


MODEL_PREFIX = os.getenv(
    "MODEL_PREFIX",
    "models/healthcare-premium-prediction/v1",
).strip("/")


# ============================================================
# MODEL VERSION
# ============================================================

# Example:
#
# MODEL_PREFIX =
# models/healthcare-premium-prediction/v1
#
# MODEL_VERSION =
# v1
#
# The version is automatically extracted from the last
# component of MODEL_PREFIX.

MODEL_VERSION = (
    MODEL_PREFIX.rstrip("/")
    .split("/")[-1]
)


# ============================================================
# PROJECT BASE DIRECTORY
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# ============================================================
# LOCAL ARTIFACT DIRECTORY
# ============================================================

LATEST_ARTIFACT_DIR = (
    BASE_DIR
    / "artifacts"
    / "latest"
)


# ============================================================
# MODEL ARTIFACT FILES
# ============================================================

# ------------------------------------------------------------
# IMPORTANT
# ------------------------------------------------------------
#
# These variable names are kept compatible with the existing
# src/prediction.py implementation.
#
# Expected local structure:
#
# artifacts/
# └── latest/
#     ├── model.pkl
#     ├── preprocessor.pkl
#     ├── metadata.json
#     └── feature_schema.json
#
# Expected S3 structure:
#
# s3://healthcare-premium-mlops-anil/
# └── models/
#     └── healthcare-premium-prediction/
#         └── v1/
#             ├── model.pkl
#             ├── preprocessor.pkl
#             ├── metadata.json
#             └── feature_schema.json
# ------------------------------------------------------------


# Main trained ML model
MODEL_FILE = "model.pkl"


# Preprocessing object
PREPROCESSOR_FILE = "preprocessor.pkl"


# Model metadata
METADATA_FILE = "metadata.json"


# Feature schema
FEATURE_SCHEMA_FILE = "feature_schema.json"


# ============================================================
# OPTIONAL FILE-NAME ALIASES
# ============================================================
#
# These aliases allow other modules to use either:
#
# MODEL_FILE
# or
# MODEL_FILE_NAME
#
# PREPROCESSOR_FILE
# or
# PREPROCESSOR_FILE_NAME
#
# This prevents naming conflicts between different modules.
# ============================================================

MODEL_FILE_NAME = MODEL_FILE

PREPROCESSOR_FILE_NAME = PREPROCESSOR_FILE

METADATA_FILE_NAME = METADATA_FILE

FEATURE_SCHEMA_FILE_NAME = FEATURE_SCHEMA_FILE


# ============================================================
# DEBUG INFORMATION
# ============================================================

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
    f"MODEL_PREFIX       : {MODEL_PREFIX}"
)

print(
    f"MODEL_VERSION      : {MODEL_VERSION}"
)

print(
    f"AWS_REGION         : {AWS_REGION}"
)

print(
    f"ARTIFACT_DIRECTORY : {LATEST_ARTIFACT_DIR}"
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