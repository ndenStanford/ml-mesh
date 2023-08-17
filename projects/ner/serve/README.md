# Overview

The `serve` image implements both the ML `ner` model serving application as well as all
accompanying test suites as defined in [the post model registry flow `Model CI pipeline (2)` of the
 continuous integration design for ML serving images](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3198812161/MLOPs).

## 1 Running the model server

To run the model server using the `docker-compose.dev.yaml` file (recommended):

- run `make projects.start/ner COMPONENT=serve ENVIRONMENT=dev`

Note: This will automatically download the model artifact if the specified output directory is
empty.

While the server is running, you can open another terminal and trigger the API. For example:

```
curl -X 'POST' 'http://0.0.0.0:8000/v1/model/ner/predict' -H 'Content-Type: application/json' -d '{"configuration": {"return_pos": true, "language": "en"}, "inputs": {"content": "Google is cool"}}'
```

Which will output:

```
{"outputs":{"predicted_content":[{"entity_type":"ORG","entity_text":"Google","score":0.9729547,"sentence_index":0,"start":0,"end":6}]}}
```
## 2 Testing the model server

The following test suites are currently implemented:

- `unit`
- `integration`
- `functional`
- `load`

A load test suite will be implemented once the `serving` library has been extended to support an
internally consistent load testing framework.

### 2.1 Run `unit` tests

`unit` test scope:
  - Code only
  - no `neuron` device dependency
  - no model artifact dependency
  - no model server will be run

To run the `unit` tests for the `serve` component, simply run:

```bash
make projects.unit/ner COMPONENT=serve ENVIRONMENT=dev
```

### 2.2 Run `integration` tests

`integration` test scope:
  - Code + ML model dependency
  - requires `neuron` device
  - requires model artifact
  - no model server will be run


To run the `integration` tests for the `serve` component, simply run:

```bash
make projects.integration/ner COMPONENT=serve ENVIRONMENT=dev
```

Note: This will automatically download the model artifact if the specified output directory is
empty.

### 2.3 Run `functional` tests

`functional` test scope:
  - Code + Ml model dependency
  - requires `neuron` device in `serve` server component
  - requires model artifact in `serve` server component
  - model server will be run in `serve` component
  - additional client will be run in `serve-functional` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network

To run the `functional` tests for the `serve` component, simply run:

```bash
make projects.functional/ner COMPONENT=serve ENVIRONMENT=dev
```

Note: This will automatically download the model artifact if the specified output directory is
empty.

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
make projects.load/ner COMPONENT=serve ENVIRONMENT=dev
```

## 3 Uploading results

To upload our results to Neptune/S3 run:

```bash
make projects.start/ner COMPONENT=serve-upload-results ENVIRONMENT=dev
```
