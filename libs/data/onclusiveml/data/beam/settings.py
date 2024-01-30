"""Settings."""

# 3rd party libraries
from apache_beam.options.pipeline_options import PipelineOptions
from pydantic import SecretStr

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings


class PipelineSettings(OnclusiveBaseSettings):
    """Pipeline settings."""

    job_name: str
    runner: str = "PortableRunner"
    streaming: bool = False
    artifact_endpoint: str = "jobserver:8098"
    job_endpoint: str = "jobserver:8099"
    environment_type: str = "LOOPBACK"
    sdk_worker_parallelism: int = 1

    def to_pipeline_options(self) -> PipelineOptions:
        """Returns `PipelineOptions` object from pipeline settings."""
        options = [
            f"--runner={self.runner}",
            f"--job-name={self.job_name}",
            f"--artifact_endpoint={self.artifact_endpoint}",
            f"--job_endpoint={self.job_endpoint}",
            f"--environment_type={self.environment_type}",
            f"--sdk_worker_parallelism={self.sdk_worker_parallelism}",
            "--worker_harness_container_image=none",
        ]
        if self.streaming:
            options += ["--streaming"]
        if self.environment_type == "EXTERNAL":
            options += ["--environment_config=localhost:50000"]
        return PipelineOptions(options)


class EnrichmentPipelineSettings(OnclusiveBaseSettings):
    """Enrichment Pipeline Settings."""

    host: str
    namespace: str
    version: str
    api_key: SecretStr
    secure: bool
