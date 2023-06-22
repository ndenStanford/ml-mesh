# Overview

The `serve` image implements both the ML `keywords` model serving application as well as all
accompanying test suites as defined in [the post model regsitry flow of the continuous integration
design for ML serving images](https://onclusive01-my.sharepoint.com/:w:/r/personal/sebastian_scherer_onclusive_com/Documents/RFC%20-%20ML%20CI%20pipeline%20framework.docx?d=w74da3073c12b412a9f8b8acd8f741dbe&csf=1&web=1&e=mJXG6p).

## 1 Running the model server

This section outlines the 4 main steps involved in running a configured `keywords` ML model server.

### 1.1 Downloading a compiled keywords model

To run `integration` and `functional` tests, as well as running the `serve` component at all, you
will need to have model version of a compiled keywords model available on your machine.

The easiest way to achieve this is to use the `tracking` library to download a given model version
frrom the model registry. For example to

- download [the model version `KEYWORDS-COMPILED-88`](https://app.neptune.ai/o/onclusive/org/keywords/models?shortId=KEYWORDS-COMPILED-88&type=modelVersion&path=.) and
- saved it locally in the `projects/keywords/serve/models/keywords_model_88` directory, run

```python
from onclusiveml import tracking

# initialize client for specific model version
mv = tracking.TrackedModelVersion(
  project="onclusive/keywords",
  model="KEYWORDS-TRAINED",
  with_id="KEYWORDS-COMPILED-88"
)

# download all model artifacts for the model version to local
mv.download_directory_from_model_version(
  local_directory_path='projects/keywords/serve/models/keywords_model_88',
  neptune_attribute_path="model"
)

# shutdown client
mv.stop()
```

Note: Make sure you have exported the `NEPTUNE_API_TOKEN` environment variable before.

This will download all model artifacts for the specified model version `KEYWORDS-COMPILED-88` to
your local directory `projects/keywords/serve/models/keywords_model_88`, creating it if it doesnt
already exist. You can then later reference that directory to ensure the relevant processes can
find the model artifacts required to serve the `keywords` model (see below sections).

### 1.2 Configuring the served model

The `ServedKeywordsModel` subclasses the `serving` library's `ServedModel` to provide the required
interface with the model server (see below section). In particular, implements:

- the `load` method to load in all required model artifacts from the local disk
  - all relevant file locations are automatically derived via the `ServedModelParams` and
    `ServedModelArtifacts` settings classes in the `serving_params` module
- the `predict` method to score the loaded `CompiledKeyBERT` model instance on validated input data,
  auto-validating the output predictions data, too
  - it uses the custom data model classes `PredictRequestModel` and `PredictResponseModel` to do
    said validation
- the `bio` method to make the loaded ML model's meta data accessible via an endpoint
  - it uses the custom data model class `BioResponseModel` to validate the outgoing Ml model meta
    data

To ensure the `load` method works as expected, all required artifact files (see previous section)
referenced in the `ServedModelParams` class need to be accessible on the local disk (including
mounted volumes in a `Docker` or `K8s` setting). These can be specified via the corresponding
environment variable `onclusiveml_serving_model_directory` .

### 1.3 Configuring the model server

The keywords model server is implemented using the internal `serving` library's `ModelServer` class.
It is configured entirely by an `ServingParams` instance taken from the `serving` library. The
recommended way to configure the `keywords` model server is therefore to use the corresponding
environment variables, as described in the `serving` library documentation.

### 1.4 Running the model server

To run the model server locally without containers:

- make sure you are in the `/projects/keywords/serve` directory
- run `python -m src.model_server`

To run the model server using the `docker-compose.dev.yaml` file:

- run `make projects.start/keywords COMPONENT=serve`

## 2 Testing the model server

The following test suites are currently implemented:

- `unit`
  - Code only
  - no `neuron` device dependency
  - no model artifact dependency
  - no model server will be run
- `integration`
  - Code + ML model dependency
  - requires `neuron` device
  - requires model artifact
    - requires completing steps `1.1` and `1.2`
  - no model server will be run
- `functional`
  - Code + Ml model dependency
  - requires `neuron` device in `serve` server component
  - requires model artifact in `serve` server component - requires completing steps `1.1` and `1.2`
  - model server will be run in `serve` component
    - requires completing step `1.3`
  - additional client will be run in `serve-integration` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network

A load test suite will be implemented once the `serving` library has been extended to support an
internally consistent load testing framework.

### 2.1 Run `unit` tests

To run the `unit` tests for the `serve` component, simply run:

```bash
make projects.unit/keywords COMPONENT=serve ENVIRONMENT=dev
```

### 2.2 Run `integration` tests

To run the `integration` tests for the `serve` component, simply run:

```bash
make projects.integration/keywords COMPONENT=serve ENVIRONMENT=dev
```

### 2.3 Run `functional` tests

To run the `functional` tests for the `serve` component, simply run:

```bash
make projects.functional/keywords COMPONENT=serve ENVIRONMENT=dev
```
