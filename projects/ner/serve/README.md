# Overview

The `serve` image implements both the ML `ner` model serving application as well as all
accompanying test suites as defined in [the post model registry flow `Model CI pipeline (2)` of the
 continuous integration design for ML serving images](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3198812161/MLOPs).

## 1 Running the model server

To run the model server using the `docker-compose.dev.yaml` file (recommended):

- run `make projects.start/ner COMPONENT=serve ENVIRONMENT=dev`

Note: This will automatically download the model artifact if the specified output directory is
empty.

## 2 Testing the model server

The following test suites are currently implemented:

- `unit`
- `integration`
- `functional`

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
