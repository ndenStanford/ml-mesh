# The `serve` component

This document outlines how to run and test your project's `serve` component.

## 1 Scope of the `serve` component

### 1.1 Overview

The `${PROJECT_NAME}-serve` container image provides the code and runtime environment for
- retrieving a compiled model / pipeline from our neptune AI model registry
  - if applicable - see below
- serving a model **owned & maintained internally** by the ML team
- uploading test results to the neptune AI model registry
  - if applicable - see above

The model in question can be a
- (trained &) compiled ML model with artifact files that are stored in the AI model registry, as is
   the case for
  - `keywords`
  - `sentiment`
  - `ner`,
  or
- "code-only" model without artifact files and no AI model registry entry, as is the case for
  - `lsh`

The python module implementing the serving process is `src/serve/model_server.py`.

It draws its configurations from the `src/serve/params.py` module, which parses all required
environment variable from the environment.

### 1.2 References

Projects implementing a `serve` component are
- `keywords`
- `lsh`

To follow the instructions in this guide, run

```bash
export PROJECT_NAME=your_project_name_here
export BASE_IMAGE_TAG=the_base_image_docker_tag_here
export IMAGE_TAG=your_desired_train_container_docker_tag_here
export NEPTUNE_API_TOKEN=your_personal_neptune_api_token_here
export AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
```

or update your `.envrc` file accordingly.

For reference implementations of all below concepts, i.e.,
- `Dockerfile` structure
- `config` directory and `dotenv` configuration files
- `src` directory and source code layout
- `test` suite implementations
- `docker compose` files and services for `dev` and `ci`

**see the [`keywords` project's `serve` component directory](https://github.com/AirPR/ml-mesh/tree/develop/projects/keywords/serve) and [corresponding docker compose service entries](https://github.com/AirPR/ml-mesh/blob/35d007edb24e90797a2b0bf357ca67a49bbf301d/projects/keywords/docker-compose.dev.yaml#L198).**



## 2 Running the `serve` component

### 2.1 Without containers (initial development and debugging only)

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

### 2.2 With containers (recommended approach)

#### 2.2.1 Building the docker container

To locally build the image
- using the ${BASE_IMAGE_TAG} version of the base image, and
- tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-serve:${IMAGE_TAG}`, run
the `make` target:

```bash
make projects.build/${PROJECT_NAME} \
  COMPONENT=serve \
  ENVIRONMENT=dev \
  BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
  IMAGE_TAG=${IMAGE_TAG}
```

#### 2.2.2 Running the components inside docker

Before running the `serve` container for a model that has artifacts associated with it, you will
first need to retrieve the model artifact from the neptune AI model registry. This will create an
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

1. Update the `serve-download` and `serve` services in your `docker compose` file accordingly
2. Run the `serve` container's model download function:

```bash
make projects.start/${PROJECT_NAME}-download-model \
   COMPONENT=serve \
   ENVIRONMENT=dev \
   IMAGE_TAG=${IMAGE_TAG}
```
3. Check the model artifacts are located in the right location
4. Run the `serve` container:

```bash
make projects.start/${PROJECT_NAME} COMPONENT=serve ENVIRONMENT=dev IMAGE_TAG=${IMAGE_TAG}
```

## 3 Testing the `serve` component

To validate every change on the component, test suites should be run using the
`docker-compose.dev.yaml` file. The following test suites are implemented:

- `unit` (mandatory)
- `integration` (optional)
- `functional` (optional)
- `load` (optional)

### 2.1 Run `unit` tests

`unit` test scope:
  - Code only
  - *no* hardware device dependency
  - *no* model artifact dependency
  - *no* model server will be run

To run the `unit` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/{$PROJECT_NAME} COMPONENT=serve ENVIRONMENT=dev IMAGE_TAG=${IMAGE_TAG}
```

### 2.2 Run `integration` tests

`integration` test scope:
  - Code + ML model dependency
  - requires access to custom hardware device(s) where applicable
    - e.g. neuron, GPU
  - requires model artifact
  - *no* model server will be run


To run the `integration` tests for the `serve` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/{$PROJECT_NAME} COMPONENT=serve ENVIRONMENT=dev IMAGE_TAG=${IMAGE_TAG}
```

### 2.3 Run `functional` tests

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
make projects.functional/{$PROJECT_NAME} COMPONENT=serve ENVIRONMENT=dev IMAGE_TAG=${IMAGE_TAG}
```

### 2.4 Run `load` tests

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
make projects.load/{$PROJECT_NAME} COMPONENT=serve ENVIRONMENT=dev IMAGE_TAG=${IMAGE_TAG}
```
