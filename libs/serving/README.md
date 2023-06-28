# 1 Overview

The `serving` library provides a tested framework to consistently implement and serve both ML
`apps` and `projects`. The utilities it provides include - but are not limited to:

- a fully configurable `ModelServer` class for hosting REST-based apis with and without ML models
  - leverages `fastapi` to [auto-generate customized endpoint swagger docs](https://fastapi.tiangolo.com/features/#automatic-docs)
- a `ServedModel` base class for subclassing to more easily integrate arbitrary model frameworks
  - outlines requirements for `predict` and `bio` method implementations of child class to ensure
    compatibility with the `ModelServer` class
- a set of utilities for
  - consistent endpoint url conventions
  - consistent endpoint data models
  - auto-generation of REST based `fastapi` routers implementing the above two:
    - `get_liveness_router`
    - `get_readiness_router`
    - `get_root_router`
    - `get_model_predict_router`
    - `get_model_bio_router`

## 2 Configuration

TBC - see `ServingParams` and its attribute classes in the `rest.params`module for now

- `UvicornSettings`
  - a [uvicorn configuration](https://github.com/encode/uvicorn/blob/master/uvicorn/config.py) specification; serving process configuration - see the `serving` library documentation for details

## 3 ModelServer

TBC - see

- the `ModelServer` class in the `rest.serve.model_server.py` module and
- the `model_server_test.py` suites in the `unit` & `integration` test suites for now

## 4 ServedModel

TBC - see

- the `ServedModel` base class in the `rest.serve.served_model.py` module,
- the `model_server_test.py` suites in the `unit` & `integration` test suites, and
- the `served_model_test.py` suites in the `unit` & `integration` test suites, and

for now

## Testing

### Unit

- Install the library
- Run `make libs.unit/serving`

### Integration

- Install the library
- Run `make libs.integration/serving`

### Functional

Since the core feature of this library is to help implement (ML) server runtimes, the functional
test requires a `server <-> client` setup, implying 2 parallel processes. This is not achievable in
the current `libs` functional test approach of simple `pytest` suites, so for now the
`functional` test suite will be disabled in the CI for `serving`. The below shows how to run it
manually on local.

- Install the library
  - `make libs.install/serving`
- Start the model server by running the `server` side test suite
  - `python -m pytest libs/serving/onclusiveml/tests/functional -ra -vv --capture=no -m server`
  - This will run on port 8000 by default, so make sure the port is free
- Run the `client` side regression test suite
  - `python -m pytest libs/serving/onclusiveml/tests/functional -ra -vv --capture=no -m client`
- Make sure to stop (`ctrl+c`) the `server` side test process once you are done testing
