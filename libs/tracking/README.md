# 1 Overview

The `tracking` library provides utilities to consistently interact with the ML team's
[neptune.ai platform](https://app.neptune.ai/o/onclusive/-/projects).

Specifically, at its core - at the time of writing, it provides a customized `TrackedModelVersion`
class that enables more functional upload/download behaviour of files, directories and dictionary
python objects, as well as the ability to configure S3 buckets as the storage backend rather than
the neptune ai servers.

The below is a minimal documentation covering

- configuration of the tracking library
- creating a model registry client for a new or existing model version
- uploading and downloading artifacts to and from an existing model version

For all three sections, see the extensive integration test suite at `tests/integration/...` for more
details.

## 2 Configuration

There are two main areas that can be configured:

- logging
- storage backend

All configurable parameters in the above two areas can be accessed via environment variables
prefixed with `onclusiveml_tracking_...`. See the `tracked_settings.py` module for more details.

### 2.1 Configuring logging

The following parameters and their environment variables are available for configuration. For more
details, see the `TrackingLibraryLoggingSettings` in the `tracking_settings.py` module.

- `name`: str

  - Role: the `name` attribute of the `tracking` library level logger python object
  - Setting
    - via env var `ONCLUSIVEML_TRACKING_LOGGER_NAME`

- `fmt`: str
  - Role: the logging message format for all tracking library logging outputs.
  - Setting
    - via env var `ONCLUSIVEML_TRACKING_LOGGER_FMT`
- level: int
  - Role: the level of logging for the tracking library logger. Takes natural log levels 10, 20,
    ... for `DEBUG`, `INFO`, ..., respectively.
  - Setting
    - via env var `ONCLUSIVEML_TRACKING_LOGGER_LEVEL`

### 2.2 Configuring storage backend

By default, the tracking library will upload all files and objects to internal S3 buckets.

The following parameters and their environment variables are available for configuration. For more
details, see the `TrackingLibraryS3Backends` and `TrackingLibraryBackendSettings` classes in the
`tracking_settings.py` module. All below environment variables are case-**in**sensitive

- `use_s3_backend`: str
  - Role: the `name` attribute of the `tracking` library level logger python object
  - Setting:
    - via env var `ONCLUSIVEML_TRACKING_BACKEND_USE_S3_BACKEND`
    - via the `use_s3_backend` argument in any initialized `TrackedModelVersion` instance's `configure_s3_storage_backend` method
    - This parameter alone can also be set via the `use_s3` argument of every
      `TrackedModelVersion.upload_...` method call. If not specified there, it will default to the
      `TrackedModelVersion` instance's configuration's `use_s3_backend` parameter value
- `s3_backend_bucket`: str
  - Role: the logging message format for all tracking library logging outputs. Defaults to the
    `core` library's `LogFormat.DETAILED.value`
  - Setting
    - via env var `ONCLUSIVEML_TRACKING_BACKEND_S3_BACKEND_BUCKET`
    - via the `s3_backend_bucket` argument in any initialized `TrackedModelVersion`
      instance's `configure_s3_storage_backend` method
- `s3_backend_prefix`: str
  - Role: the level of logging for the tracking library logger. Takes natural log levels 10, 20,
    ... for `DEBUG`, `INFO`, ..., respectively.
  - Setting
    - via env var `ONCLUSIVEML_TRACKING_BACKEND_S3_BACKEND_PREFIX`
    - via the `s3_backend_prefix` argument in any initialized `TrackedModelVersion`
      instance's `configure_s3_storage_backend` method.

NOTE:

- Calling the `configure_s3_storage_backend` method will **only** affect that specific `TrackedModelVersion` instance's
  storage backend configuration
- Calling any `TrackedModelVersion.upload_...` method while specifying the `use_s3` argument will **only**
  affect that specific upload

## 3 Custom model version client

The main class for interacting with the neptune ai model registry is the `TrackedModelVersion`
class. It is configurable w.r.t storage backends (see above) and provides consistent and tested
utilities to upload and download artifacts to and from specified neptune projects and model
(versions).

### 3.1 Creating a model version client

To create a `TrackedModelVersion` instance directly, simply call the constructor:

```python
test_model_version = TrackedModelVersion(
        model="TES-TEST",
        project="onclusive/test",
        api_token=os.environ.get("NEPTUNE_API_TOKEN"),  # your credentials
    )
```

Since it is subclassed from `neptune`'s `ModelVersion`, you can also pass additional `kwargs`, for
example to reference an existing model version and pin the client `mode` to `read-only`:

```python
test_model_version = TrackedModelVersion(
        model="TES-TEST",
        with_id="TES-TEST-101,
        project="onclusive/test",
        api_token=os.environ.get("NEPTUNE_API_TOKEN"),  # your credentials
        mode="read-only",
    )
```

When finished, stop the client by running

```python
test_model_version.stop()
```

to force a sync with the remote servers and sever the client connection. See the neptune AI docs for
more details:

- [model version](https://docs.neptune.ai/api/model_version/)
- [model version modes](https://docs.neptune.ai/api/connection_modes/)

See also the example used in the integration test conftest at `tests/integration/conftest.py`.

NOTE: The constructor of the `TrackedModelVersion` class reads in the storage backend configuration via
environment variables, but lets you reconfigure it at runtime via the `configure_s3_storage_backend`
method -see section `2.2 Configuring storage backend`.

### 3.2 Model version upload utilities

Below is a list of client methods supporting the upload of individual files, directories and python
dictionary objects, respectively.

- `tracked_model_version.upload_file_to_model_version`
  - supports the upload of either a file on local disk, or a `neptune.File` object
- `tracked_model_version.upload_directory_to_model_version`
  - supports the upload of an entire directory on local disk
  - will automatically convert all involved local files' paths to corresponding neptune attribute
    paths
  - allows configuration of files to ignore via the `exclude` argument. By default, will ignore
    hidden files (starting with `.`) and dunder files (starting with `__`)
- `tracked_model_version.upload_config_to_model_version`
  - supports the upload of a specified python dictionary object. Will carry out intermediary
    conversions to `.json` type, so python dictionary key and value types will have to be
    compatible

Note:

- all above methods can be configured at the call level to use/not use S3 storage backends by
  setting the `use_s3` argument to `True/False`
- all above methods require the `neptune_attribute_path` string type argument to specify which
  reference the resulting artifact will receive on the neptune model registry's model version
  entry
- for more details on how to use these, see the `upload` integration test sub-suite in
  `tests/integration/tracked_model_version/uploads_test.py`

### 3.3 Model version download utilities

Below is a list of client methods supporting the download of individual files, directories and python
dictionary objects, respectively.

- `tracked_model_version.download_file_from_model_version`
  - supports the download of a neptune model version attribute that was the result of a call to
    `tracked_model_version.upload_file_to_model_version`
- `tracked_model_version.download_directory_from_model_version`
  - supports the download of a neptune model version attribute that was the result of a call to
    `tracked_model_version.upload_directory_to_model_version`
  - will automatically convert all involved neptune attributes' paths to the corresponding local
    file paths
- `tracked_model_version.download_config_from_model_version`
  - supports the download of a neptune model version attribute that was the result of a call to
    `tracked_model_version.upload_config_to_model_version`
  - returns the config as a python dictionary object, but uses and intermediary file on local disk
    for the actual download

Note:

- all above methods require the `neptune_attribute_path` string type argument to specify which
  artifact of the given model version you are referencing
- for more details on how to use these, see the `download` integration test sub-suite in
  `tests/integration/tracked_model_version/downloads_test.py`

## 4 Tracking utilities

The library also provides some `pydantic.BaseSetting` utilities to help keep neptune ai model
version entries consistent as well as track Github Action contexts for CI lineage capability.

For more details, see the respective clases in the `tracked_model_utils.py` module.

### 4.1 Model version

A simple utility capturing the required `kwargs` of the `(Tracked)ModelVersion` class from
designated environment variables. Supports the suppression of the sensitive `NEPTUNE_API_TOKEN`
parameter.

### 4.2 ModelCard

The `TrackedModelCard` class is a template for an ID card that **should get added to every model
submitted to the neptune AI model registry**.

**It should always be referenced under the neptune
attribute path `model/model_card`**.

It contains meta data on various hyperparameters on a given model as appropriate (e.g. compilation
settings for a `compiled` type model), as well as neptune attribute path references to other key
artifacts of that model version.

It also includes by default another utility class, the `TrackedGithubActionsSpecs` (see next
section).

### 4.3 CI lineage

The `TrackedGithubActionsSpecs` class serves captures [all Github Actions CI related environment
variables](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables)
and provides an easy and consistent means to attach this CI runtime context to model registry
entries via the `TrackedModelCard`. It will be included by default and fall back on dummy values
for each unspecified parameter.
