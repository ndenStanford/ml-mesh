# 1 Overview

The `serving` library provides a tested framework to consistently

- implement and serve, as well as
- load test

both ML `apps` and `projects` REST API services. The utilities it provides are split into two
main modules:

- `rest.serve`
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
- `rest.testing`
  - a load test configuration class `LoadTestingParams` definine
    - client behaviour,
    - load test duration,
    - client pool size
    - etc.
  - a fully configurable (via `LoadTestParams`) `LoadTest` class to run a [locust](https://locust.io/)-based
    load test within a python session and obtain structured performance reports via the `report`
    method and `TestReport` class
  - a `LoadTestCriteria` class to define and evaluate performance requirements via the
    `Criterion` and `EnvironmentCriterion` classes, either in code or purely through environment
    variables, against a `LoadTest` instance's `TestReport` output

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



## 5 `LoadTest`

To instantiate a configured load test to
- ping the `GET` type endpoint `http://github.com`
- run for `20s`
- use `10` test clients
- build the client pool at a rate of `2 clients/second` until it reaches the desired 10 and starts
  the test

run

```python

# define client behaviour
class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task()
    def get_home_page(self):
        """
        Gets /
        """
        self.client.get("/")

load_test_settings = LoadTestingParams(
        user_classes=[WebsiteUser],
        locustfile="",
        host="http://github.com",
        run_time="20s",
        num_users=10,
        spawn_rate=2,
        reset_stats=True,
    )

load_test = LoadTest(settings=load_test_settings)
```

To run the load test you just created, run

```python
load_test.run()
```

To generate a report for the load test you just ran, run

```python
report = load_test.report()
```

To export the report as a `json` file, run

```python
import json

with open("report.json","w") as report_file:
  json.dump(report.json(),report_file)

## 6 `LoadTestCriteria`

To create a `LoadTestCriteria` instance that
- ensures the average latency is below 50ms against the `GET`-type `http://github.com` endpoint, and
- ensures the average failure rate is below 5% against the `GET`-type `http://github.com` endpoint

run

```python
from serving.rest.testing import (
  ValidEndpointTypes,
  Criterion,
  LoadTestCriteria
)

criteria = [
  Criterion(
      name=ValidMeasurements.avg_response_time.value,
      threshold=50,
      endpoint_type=ValidEndpointTypes.get.value,
      endpoint_url="http://github.com",
      ensure_lower=True,
  ),
  Criterion(
      name=ValidMeasurements.failures_percent.value,
      threshold=0.05,
      endpoint_type=ValidEndpointTypes.post.value,
      endpoint_url="http://github.com",
      ensure_lower=True,
  ),
]

load_test_criteria = LoadTestCriteria(criteria=criteria)
```

To evaluate your report you defined in the previous section against the criteria, run

```
evaluation = load_test_criteria.evaluate(report)
```

To export the evaluation results as a `json` file, run

```python
import json

with open("evaluation.json","w") as evaluation_file:
  json.dump(evaluation.json(),evaluation_file)
```

## Testing

### Unit

Coverage: `serve` and `testing` modules

- Install the library
- Run `make libs.unit/serving`

### Integration

Coverage: `serve` and `testing` modules

- Install the library
- Run `make libs.integration/serving`

### Functional

Coverage: `serve` module only. `testing` coverage is completely achieved in the `unit` and
`integration` suites.

Since the core feature of this library's `serve` module is to help implement (ML) server runtimes,
the functional test requires a `server <-> client` setup, implying 2 parallel processes. This is not
 achievable in the current `libs` functional test approach of simple `pytest` suites, so for now the
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
