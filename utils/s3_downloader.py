import shutil

import boto3

from botocore.exceptions import ClientError

from config.settings import (
    MODEL_BUCKET,
    MODEL_PREFIX,
    AWS_REGION,
    LATEST_ARTIFACT_DIR,
)


# ============================================================
# MODEL ARTIFACT FILES
# ============================================================

FILES = [
    "model.pkl",
    "preprocessor.pkl",
    "metadata.json",
    "feature_schema.json",
]


class S3ModelDownloader:

    def __init__(self):

        print("=" * 70)
        print("S3 MODEL DOWNLOADER CONFIGURATION")
        print("=" * 70)

        print(f"S3 Bucket : {MODEL_BUCKET}")
        print(f"S3 Prefix : {MODEL_PREFIX}")
        print(f"AWS Region: {AWS_REGION}")

        print("=" * 70)

        self.client = boto3.client(
            "s3",
            region_name=AWS_REGION,
        )


    # ========================================================
    # CHECK IF ALL ARTIFACTS EXIST LOCALLY
    # ========================================================

    def artifacts_exist(self):

        return all(
            (LATEST_ARTIFACT_DIR / file).exists()
            for file in FILES
        )


    # ========================================================
    # DOWNLOAD MODEL ARTIFACTS
    # ========================================================

    def download(self):

        # ----------------------------------------------------
        # Check local artifacts
        # ----------------------------------------------------

        if self.artifacts_exist():

            print("Artifacts already exist.")
            print("Skipping S3 download.")

            return


        print("=" * 70)
        print("Downloading model artifacts from S3")
        print("=" * 70)

        print(f"S3 Bucket : {MODEL_BUCKET}")
        print(f"S3 Prefix : {MODEL_PREFIX}")
        print(f"AWS Region: {AWS_REGION}")

        print("=" * 70)


        # ----------------------------------------------------
        # Remove old/incomplete artifacts
        # ----------------------------------------------------

        if LATEST_ARTIFACT_DIR.exists():

            print(
                f"Removing existing artifact directory: "
                f"{LATEST_ARTIFACT_DIR}"
            )

            shutil.rmtree(
                LATEST_ARTIFACT_DIR
            )


        # ----------------------------------------------------
        # Create artifact directory
        # ----------------------------------------------------

        LATEST_ARTIFACT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )


        try:

            # ------------------------------------------------
            # Download every artifact
            # ------------------------------------------------

            for file in FILES:

                # Safely construct S3 key
                key = (
                    f"{MODEL_PREFIX.rstrip('/')}"
                    f"/{file}"
                )


                local_path = (
                    LATEST_ARTIFACT_DIR
                    / file
                )


                print()
                print("-" * 70)
                print(f"Downloading : {file}")
                print(f"S3 Bucket  : {MODEL_BUCKET}")
                print(f"S3 Key     : {key}")
                print(f"Local Path : {local_path}")
                print("-" * 70)


                self.client.download_file(
                    MODEL_BUCKET,
                    key,
                    str(local_path),
                )


                print(
                    f"Successfully downloaded: {file}"
                )


            # ------------------------------------------------
            # Download completed
            # ------------------------------------------------

            print()
            print("=" * 70)
            print("All model artifacts downloaded successfully.")
            print("=" * 70)


        except ClientError as e:

            # ------------------------------------------------
            # Delete incomplete download
            # ------------------------------------------------

            shutil.rmtree(
                LATEST_ARTIFACT_DIR,
                ignore_errors=True,
            )


            print()
            print("=" * 70)
            print("S3 MODEL DOWNLOAD FAILED")
            print("=" * 70)

            print(f"S3 Bucket : {MODEL_BUCKET}")
            print(f"S3 Prefix : {MODEL_PREFIX}")
            print(f"AWS Region: {AWS_REGION}")

            print(f"AWS Error : {e}")

            print("=" * 70)


            raise RuntimeError(
                f"Unable to download artifacts from S3: {e}"
            ) from e