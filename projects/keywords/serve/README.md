# Overview

The `serve` image implements both the ML `keywords` model serving application as well as all
accompanying test suites as defined in [the post model registry flow `Model CI pipeline (2)` of the
 continuous integration design for ML serving images](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3198812161/MLOPs).

## 0 Downloading the model

See the `serve-download-model` docker compose service entry for the required environment variables, and make sure they are exported in the terminal before proceeding.

To download a model from the neptune model registry using the `docker-compose.dev.yaml` file, run:

```bash
make projects.start/keywords COMPONENT=serve-download-model
```

This will download the specified model version into a versioned subdirectory of the `projects/keywords/serve/models` directory.

Note: This is a **required** step before running the model server and some test suites locally. On
K8s, the provisioning of model artefacts to the serving pod is done via a push mechanism to the
shared EFS before deployment. The relevant EFS directory is then mounted onto the serving pod & underlying serving container. For consistency, this approach uses the same environment variables to find the model artefacts on the local disk from within the `serve` container as the local development and CI docker compose files.


## 1 Running the model server

To run the model server using the `docker-compose.dev.yaml` file, run:

```bash
make projects.start/keywords COMPONENT=serve ENVIRONMENT=dev
```

## 2 Testing the model server

The following test suites are implemented:

- `unit`
- `integration`
- `functional`
- `load`


### 2.1 Run `unit` tests

`unit` test scope:
  - Code only
  - *no* `neuron` device dependency
  - *no* model artifact dependency
  - *no* model server will be run

To run the `unit` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/keywords COMPONENT=serve ENVIRONMENT=dev
```

### 2.2 Run `integration` tests

`integration` test scope:
  - Code + ML model dependency
  - requires `neuron` device
  - requires model artifact
  - *no* model server will be run


To run the `integration` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/keywords COMPONENT=serve ENVIRONMENT=dev
```

### 2.3 Run `functional` tests

`functional` test scope:
  - Code + Ml model dependency
  - requires `neuron` device in `serve` server component
  - requires model artifact in `serve` server component
  - model server will be run in `serve` component
  - additional client will be run in `serve-functional` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network

To run the `functional` tests for the `serve` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/keywords COMPONENT=serve ENVIRONMENT=dev
```

### 2.4 Run `load` tests

`load` test scope:
  - Code + Ml model dependency
  - requires `neuron` device in `serve` server component
  - requires model artifact in `serve` server component
  - model server will be run in `serve` component
  - additional client will be run in `serve-load` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network
  - export of 4 `json` files into ``projects/keywords/serve/models/{$NEPTUNE_MODEL_VERSION_ID}/{$IMAGE_TAG}/test_results` directory:
    - `load_test_report.json`: The performance metrics captured during the load test
    - `load_test_evaluation.json`: Individual and final fail/pass outcomes against specified
    - `serve_image_spec.json`: The full name and tag of the `serve` docker image used
    - `github_action_context.json`: Github Action CI runtime context meta data
      criteria

To run the `load` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.load/keywords COMPONENT=serve ENVIRONMENT=dev
```

ci trigger
