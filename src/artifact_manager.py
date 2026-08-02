import logging
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.config import (
    AWS_REGION,
    MODEL_BUCKET,
    MODEL_PATH,
    ARTIFACT_DIR,
    MODEL_FILE,
    PREPROCESSOR_FILE,
    METADATA_FILE,
    FEATURE_SCHEMA_FILE,
)


# ==========================================================
# Logging
# ==========================================================

logger = logging.getLogger(__name__)


# ==========================================================
# S3 CLIENT
# ==========================================================

def get_s3_client():
    """
    Create and return an S3 client.

    AWS credentials are automatically resolved by boto3.

    Local development:
        - AWS CLI credentials
        - Environment variables
        - AWS profiles

    Kubernetes/EKS:
        - EKS Pod Identity
        - IRSA
    """

    return boto3.client(
        "s3",
        region_name=AWS_REGION,
    )


# ==========================================================
# S3 KEY
# ==========================================================

def get_s3_key(
    filename: str,
) -> str:
    """
    Build the complete S3 object key.

    Example:

        MODEL_PATH:
            models/healthcare-premium-prediction/v1

        filename:
            model.pkl

        Result:
            models/healthcare-premium-prediction/v1/model.pkl
    """

    if not MODEL_PATH:
        raise ValueError(
            "MODEL_PATH environment variable "
            "is not configured."
        )

    return (
        f"{MODEL_PATH.strip('/')}"
        f"/{filename}"
    )


# ==========================================================
# DOWNLOAD SINGLE FILE
# ==========================================================

def download_file_from_s3(
    s3_client,
    filename: str,
    destination_path: Path,
):
    """
    Download a single artifact from S3.
    """

    if not MODEL_BUCKET:
        raise ValueError(
            "MODEL_BUCKET environment variable "
            "is not configured."
        )

    s3_key = get_s3_key(
        filename
    )

    logger.info(
        "Downloading S3 artifact: "
        "s3://%s/%s",
        MODEL_BUCKET,
        s3_key,
    )

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:

        s3_client.download_file(
            MODEL_BUCKET,
            s3_key,
            str(destination_path),
        )

        logger.info(
            "Successfully downloaded %s "
            "to %s",
            filename,
            destination_path,
        )

    except (
        ClientError,
        BotoCoreError,
    ) as exc:

        logger.error(
            "Failed to download artifact: "
            "s3://%s/%s",
            MODEL_BUCKET,
            s3_key,
        )

        raise RuntimeError(
            "Unable to download S3 artifact "
            f"s3://{MODEL_BUCKET}/{s3_key}"
        ) from exc


# ==========================================================
# DOWNLOAD ALL MODEL ARTIFACTS
# ==========================================================

def download_model_artifacts() -> Path:
    """
    Download all required model artifacts from S3.

    Files:

        - model.pkl
        - preprocessor.pkl
        - metadata.json
        - feature_schema.json

    All files are downloaded to:

        artifacts/latest/

    Returns:
        Path to the local artifact directory.
    """

    logger.info(
        "Starting model artifact download "
        "from S3."
    )

    logger.info(
        "S3 bucket: %s",
        MODEL_BUCKET,
    )

    logger.info(
        "S3 model path: %s",
        MODEL_PATH,
    )

    logger.info(
        "Local artifact directory: %s",
        ARTIFACT_DIR,
    )

    # ------------------------------------------------------
    # Create local artifact directory
    # ------------------------------------------------------

    ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------
    # Create S3 client
    # ------------------------------------------------------

    s3_client = get_s3_client()

    # ------------------------------------------------------
    # Define required artifacts
    # ------------------------------------------------------

    artifacts = [

        (
            MODEL_FILE,
            ARTIFACT_DIR
            / MODEL_FILE,
        ),

        (
            PREPROCESSOR_FILE,
            ARTIFACT_DIR
            / PREPROCESSOR_FILE,
        ),

        (
            METADATA_FILE,
            ARTIFACT_DIR
            / METADATA_FILE,
        ),

        (
            FEATURE_SCHEMA_FILE,
            ARTIFACT_DIR
            / FEATURE_SCHEMA_FILE,
        ),

    ]

    # ------------------------------------------------------
    # Download each artifact
    # ------------------------------------------------------

    for (
        filename,
        destination_path,
    ) in artifacts:

        download_file_from_s3(

            s3_client=s3_client,

            filename=filename,

            destination_path=destination_path,

        )

    logger.info(
        "All model artifacts downloaded "
        "successfully."
    )

    logger.info(
        "Artifacts available at: %s",
        ARTIFACT_DIR,
    )

    return ARTIFACT_DIR


# ==========================================================
# VALIDATE ARTIFACTS
# ==========================================================

def validate_artifacts(
    artifact_dir: Path,
) -> None:
    """
    Validate that all required model artifacts
    exist locally.
    """

    artifact_dir = Path(
        artifact_dir
    )

    required_files = [

        artifact_dir
        / MODEL_FILE,

        artifact_dir
        / PREPROCESSOR_FILE,

        artifact_dir
        / METADATA_FILE,

        artifact_dir
        / FEATURE_SCHEMA_FILE,

    ]

    missing_files = [

        str(file_path)

        for file_path in required_files

        if not file_path.exists()

    ]

    if missing_files:

        logger.error(
            "Required model artifacts "
            "are missing:"
        )

        for file_path in missing_files:

            logger.error(
                "Missing artifact: %s",
                file_path,
            )

        raise FileNotFoundError(

            "Required model artifacts "
            "are missing:\n"

            + "\n".join(
                missing_files
            )

        )

    logger.info(
        "All required model artifacts "
        "are available."
    )

    logger.info(
        "Validated artifact directory: %s",
        artifact_dir,
    )