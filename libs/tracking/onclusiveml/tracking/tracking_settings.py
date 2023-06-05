# Standard Library
from enum import Enum
from typing import Dict

# 3rd party libraries
from pydantic import root_validator

# Internal libraries
from onclusiveml.core.base.params import Params
from onclusiveml.core.logging.constants import (  # noqa:F401
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    LogFormat,
)


class TrackingLibraryS3Backends(Enum):
    """Valid range of S3 storage backends for the tracking library. Originates from `ml-platform`'s
    S3 section of the `mesh` stack @
    - https://github.com/AirPR/ml-platform/blob/prod/infrastructure/stacks/mesh/s3.tf (module)
    - https://github.com/AirPR/ml-platform/blob/prod/infrastructure/stacks/mesh/.environments/...
        dev/vars.tfvars (dev)
    - https://github.com/AirPR/ml-platform/blob/prod/infrastructure/stacks/mesh/.environments/...
        stage/vars.tfvars (stage)
    - https://github.com/AirPR/ml-platform/blob/prod/infrastructure/stacks/mesh/.environments/...
        prod/vars.tfvars (prod)
    """

    dev: str = "onclusive-model-store-dev"
    stage: str = "onclusive-model-store-stage"
    prod: str = "onclusive-model-store-prod"


class TrackingLibraryLoggingSettings(Params):
    """Entrypoint to configure logging behaviour of the tracking library for the current session."""

    name: str = __name__
    fmt: str = LogFormat.DETAILED.value
    level: int = INFO  # 10=DEBUG, 20=INFO, 30=WARNING, 40=ERROR, 50=CRITICAL

    class Config:
        env_prefix = "onclusiveml_tracking_logger_"


class TrackingLibraryBackendSettings(Params):
    """
    Entrypoint to configure the tracking library's S3 storage backend behaviour via environment
    variables. The values derived by this class's attributes will be used as default values for the
    identically named TrackedModelVersion class' constructor arguments
    - use_s3_backend
    - s3_backend_bucket
    - s3_backend_prefix
    """

    use_s3_backend: bool = True
    s3_backend_bucket: str = TrackingLibraryS3Backends.dev.value
    s3_backend_prefix: str = "neptune-ai-model-registry"

    class Config:
        env_prefix = "onclusiveml_tracking_backend_"

    @root_validator
    def validate_s3_storage_settings(cls, values: Dict) -> Dict:
        """Validates the S3 storage backend configuration contained in the `values` dictionary.

        Args:
            values (Dict): Contains the following S3 storage backend configuration attributes:
                - use_s3_backend: (bool): Whether to use S3 storage as a backend for file
                    attributes. Enabling this is useful for two reasons:
                        - Storage capacity on Neptune servers is very limited at 100GB/month, and
                            LLM model artifacts will easily use up that quota when using the
                            default neptune storage servers
                        - S3 buckets configured in the same VPC/AZ as the EC2 instances hosting the
                            application code.

                - s3_backend_bucket (str, optional): The bucket to be used for file attribute
                    storage.
                - s3_backend_prefix (str, optional): The optional S3 prefix to be prepended to all
                    file attributes stored in the S3 bucket via the TrackedModelVersion utilities.

        Raises:
            ValueError: If an invalid bucket is specified (see tracking_settings for valid range)
            ValueError: If the `s3_backend_prefix` is not empty but starts/ends with a '/'

        Returns:
            Dict: A dictionary containing a validated S3 storage backend configuration
        """

        use_s3_backend = values.get("use_s3_backend")

        if use_s3_backend:
            s3_backend_bucket = values.get("s3_backend_bucket")
            s3_backend_prefix = values.get("s3_backend_prefix")
            # ensure specified bucket is valid
            if s3_backend_bucket not in (
                TrackingLibraryS3Backends.dev.value,
                TrackingLibraryS3Backends.stage.value,
                TrackingLibraryS3Backends.prod.value,
            ):
                raise ValueError(
                    f"Invalid backend storage bucket {s3_backend_bucket}: Must be one"
                    " of the valid options: "
                    f"{TrackingLibraryS3Backends.dev.value} (development environment)"
                    f"{TrackingLibraryS3Backends.stage.value} (staging environment)"
                    f"{TrackingLibraryS3Backends.prod.value} (production environment)"
                )
            # ensure validity of backend prefix
            if s3_backend_prefix and (
                s3_backend_prefix.startswith("/") or s3_backend_prefix.endswith("/")
            ):
                raise ValueError(
                    f"Invalid backend storage prefix {s3_backend_prefix}: May not start or end on "
                    '"/"'
                )
        else:
            # set both bucket and prefix specs to empty strings as they are irrelevant
            values["s3_backend_bucket"] = ""
            values["s3_backend_prefix"] = ""

        return values
