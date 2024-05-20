# The `serve` component

This document outlines how to run and test your project's `serve` component.

## 1 Scope of the `serve` component :mag_right:

### 1.1 Overview :mount_fuji:

A project's `serve` container image provides the code and runtime environment for
- retrieving a compiled model / pipeline from our neptune AI model registry
  - if applicable - see below
- serving a model **owned & maintained internally** by the ML team
- uploading test results to the neptune AI model registry
  - if applicable - see above

Each of the 3 tasks corresponds to a python module:
1. `src/util/download_compiled_model.py`
2. `src/serve/model_server.py`.
3. `src/util/upload_test_results.py`

The model in question can be a
- :factory: (trained &) compiled ML model *with artifact* files that are stored in the AI model registry, as
 is the case for
  - `keywords` :key::memo:
  - `sentiment` :smile:/:frowning:
  - `ner`, :books::arrow_forward::european_castle::church::hotel:
  or
- :speedboat: "code-only" model *without artifact* files and no AI model registry entry, as is the case for
  - `lsh` :books::arrow_forward::hash::hash:
  - `entity-fishing` :fishing_pole_and_fish:
  - `summarization` :books::arrow_forward::memo:

It draws its configurations from the `src/serve/params.py` module, which parses all required
environment variable from the environment.

## 2 Setup & references :wrench:

Projects implementing a `serve` component are
- **`keywords`** :key::memo: | :factory:
- `ner`: :books::arrow_forward::european_castle::church::hotel: | :factory:
- `sentiment`: :smile:/:frowning: | :factory:
- `lsh` :books::arrow_forward::hash::hash: | :speedboat:
- `entity-fishing` :fishing_pole_and_fish: | :speedboat:
- `summarization` :books::arrow_forward::memo:| :speedboat:

### 2.1 Environment variables :deciduous_tree:

To follow the instructions in this guide, run

```bash
export PROJECT_NAME=your_project_name_here
export BASE_IMAGE_TAG=the_base_image_docker_tag_here
export IMAGE_TAG=your_desired_serve_container_docker_tag_here
export NEPTUNE_API_TOKEN=your_personal_neptune_api_token_here
export AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
```

or update your `.envrc` file accordingly.

### 2.2 Docker compose :whale:

The following `docker compose` services are typically associated with a project's `serve`
component:
- :construction: :rocket: `serve`
  - builds the serving image
  - runs the model server process
- :warning: `serve-unit`
  - runs `unit` test suite
- :warning: `serve-integration`
  - runs `integration` test suite
- :warning: `serve-functional`
  - runs `functional` test suite
- :warning: `serve-load` (optional)
  - runs `load` test suite (if applicable)
- :rocket: `serve-upload-results` (optional)
  - uploads load test results to model registry
- :rocket: `serve-download-model` (optional)
  - downloads model from model registry (if applicable)


### 2.3 Building the `serve` component :construction:

To locally build the image
- using the `${BASE_IMAGE_TAG}` version of the base image, and
- using the `docker-compose.dev.yaml`,
- using the `development` build stage,
- tagged as `690763002009.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-serve:${IMAGE_TAG}`, run
the `make` target:

```bash
make projects.build/${PROJECT_NAME} COMPONENT=serve
```

### 2.4 Download model :arrow_double_down:

If the project has model artifacts associated with its `serve` component, you will
first need to retrieve it from the neptune AI model registry. This will create an
additional `models` directory in the `projects/${PROJECT_NAME}/serve` directory, including a
subdirectory named after the model version which includes all artifacts:

- `projects/${PROJECT_NAME}/serve/models/{some-model-version}`

For example, `projects/keywords/serve/models/KEYWORDS-COMPILED-88`.

NOTE: This is a **required** step before running the model server for every model requiring model
artifacts and some test suites locally. On K8s, the provisioning of model artefacts to the serving
 pod is done via a push mechanism to the shared EFS before deployment. The relevant EFS directory
 is then mounted onto the serving pod & underlying serving container. For consistency, this approach
  uses the same environment variables to find the model artefacts on the local disk from within the
  `serve` container as the local development and CI docker compose files.

To retrieve model artifacts and run the `serve` container locally using
- the services implemented in the `projects` `docker-compose.dev.yaml` file and
- internal `projects` level `make` & `docker compose` utilities, follow the below steps.

1. Update the `serve-download-model` (if applicable) and `serve` services in your `docker compose`
 file accordingly
2. Run the `serve` container's model download function:

```bash
make projects.run/${PROJECT_NAME} COMPONENT=serve TASK=download-model
```
3. Check the model artifacts are located in the right location

### 2.5 Example implementation :nut_and_bolt: :eyes:

For reference implementations of all below concepts, i.e.,
- `Dockerfile` structure
- `config` directory and `dotenv` configuration files
- `src` directory and source code layout
- `test` suite implementations
- `docker compose` files and services for `dev` and `ci`

see the
- [**`keywords` project's `serve` component directory**](../keywords/serve) and
- [**corresponding docker compose service entries**](https://github.com/AirPR/ml-mesh/blob/35d007edb24e90797a2b0bf357ca67a49bbf301d/projects/keywords/docker-compose.dev.yaml#L198).**

## 3 Testing the `serve` component :warning:

To validate every change on the component, test suites should be run using the
`docker-compose.dev.yaml` file. The following test suites are implemented:

- [`unit` (mandatory)](#31-run-unit-tests)
- [`integration` (mandatory)](#32-run-integration-tests)
- [`functional` (mandatory)](#33-run-functional-tests)
- [`load` (optional)](#34-run-load-tests)

You can also [test your model service manually](#35-run-manual-tests)

### 3.1 Run `unit` tests :warning: :nut_and_bolt:

`unit` test scope:
  - Code only
  - *no* hardware device dependency
  - *no* model artifact dependency
  - *no* model server will be run

To run the `unit` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/${PROJECT_NAME} COMPONENT=serve
```

### 3.2 Run `integration` tests :warning: :nut_and_bolt: :nut_and_bolt:

`integration` test scope:
  - Code + ML model dependency
  - requires access to custom hardware device(s) where applicable
    - e.g. neuron, GPU
  - requires model artifact
  - *no* model server will be run


To run the `integration` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/${PROJECT_NAME} COMPONENT=serve
```

### 3.3 Run `functional` tests :warning: :rocket: :dart:

`functional` test scope:
  - Code + Ml model dependency
  - requires access to custom hardware device(s) - where applicable - in the `serve` server
    component
    - e.g. neuron, GPU
  - requires model artifact in `serve` server component
  - model server will be run in `serve` component
  - additional client will be run in `serve-functional` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network

To run the `functional` tests for the `serve` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/${PROJECT_NAME} COMPONENT=serve
```

### 3.4 Run `load` tests :warning: :rocket: :watch:

`load` test scope:
  - Code + Ml model dependency
  - requires access to custom hardware device(s) - where applicable - in the `serve` server
    component
  - requires model artifact in `serve` server component
  - model server will be run in `serve` component
  - additional client will be run in `serve-load` component, sending genuine `http` requests
    to the model server running in `serve` over the `docker compose` network
  - export of 4 `json` files into
    `projects/${PROJECT_NAME}/serve/models/{some-model-version}/{$IMAGE_TAG}/test_results` directory:
    - `load_test_report.json`: The performance metrics captured during the load test
    - `load_test_evaluation.json`: Individual and final fail/pass outcomes against specified
    - `serve_image_spec.json`: The full name and tag of the `serve` docker image used
    - `github_action_context.json`: Github Action CI runtime context meta data
      criteria

To run the `load` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.load/${PROJECT_NAME} COMPONENT=serve
```

### 3.5 Run manual tests :warning: :hand:

Before pinging the model service, make sure it is up and running by following the instructions in [the section on starting the model server](#42-with-containers-recommended-approach)

Once the model server is running visit `http://0.0.0.0:8000/docs` for the FastAPI's interactive Swagger docs. Here you can interact with the following endpoints:

- liveness: `http://0.0.0.0:8000/v1/live`
- readiness: `http://0.0.0.0:8000/v1/ready`
- model meta data: `http://0.0.0.0:8000/v1/model/${PROJECT_NAME}/bio`
- model inference: `http://0.0.0.0:8000/v1/model/${PROJECT_NAME}/predict`

For expected results, refer to the project's `serve` component's `README.md`

Note: You might need to change the port `8000` depending on what port your `docker-compose.dev.yaml`
uses.

## 4 Running the `serve` component :rocket:

### 4.1 Without containers (initial development and debugging only)

For development purposes, the pipeline can be run locally without containers. Note that while this
could ease the development process, it has some downsides since you are now outside of your bespoke
container runtime environment. The following risks should be considered. It's important to test
the functionality of your code via make command once the development is finished.

- Some python & OS-level dependencies might be missing
- Some env vars might be missing
- The model artifact might be missing

1. Change into the `projects/${PROJECT_NAME}/serve/src` directory
   - `cd projects/${PROJECT_NAME}/serve`
2. Run the model retrieval + registering step
   - `python -m src.smodel_server`

### 4.2 With containers (recommended approach) :rocket: :whale:

To run the `serve` container locally using
- the services implemented in the `projects` `docker-compose.dev.yaml` file and
- internal `projects` level `make` & `docker compose` utilities, follow the below steps.
- a locally stored model artifact obtained by completing step
[2.4 Download model](#2.4-download-model),

#### 4.2.1 Update configuration

Update the `docker-compose.dev.yaml`'s `serve` service as needed. `docker compose` will inject the
environment variable values directly into the running container (see below) to allow for serving
 configuration updates without requiring a rebuild of the docker container.

#### 4.2.2 Serve the model

```bash
make projects.start/${PROJECT_NAME} COMPONENT=serve
```
