# The `compile` component

This document outlines how to run and test your project's `compile` component.

## 1 Scope of the `compile` component :mag_right:

### 1.1 Overview :mount_fuji:

A project's `compile` container image provides the code and runtime environment for
- retrieving a specified, uncompiled model / pipeline from the neptune AI model registry,
- compiling it to a format optimized for serving (e.g. neuron)
- validating the compiled model / pipeline via regression tests
- registering the compiled model / pipeline on our internal neptune AI model registry.

Each of the 4 steps corresponds to a (set of) python module(s):

1. `src/download_uncompiled_model.py`
2. `src/compile_model.py`
3. Regression test suite inside `src/test_compiled_model` directory:
   - `pytest.ini`
   - `conftest.py`
   - `compiled_model_test.py`
4. `src/upload_compiled_model.py`

Each component draws its configurations from the `settings.py` module, which parses all required
environment variable either

- from the environment, or, if not specified,
- from the `config/dev.env` dotenv file (locally or in the container when running inside docker)

Specs defined in the `config/prod.env` are used only during CI processes.

Orchestration & execution of these components as a model compile *pipeline* is implemented by the
`run_compile_pipeline.py` script.

## 2 Setup & references :wrench:

Projects implementing a `compile` component are
- **`keywords`** :key::memo:
- `ner` :books::arrow_forward::european_castle::church::hotel:
- `sentiment` :smile:/:frowning:

### 2.1 Environment variables :deciduous_tree:

To follow the instructions in this guide, run

```bash
export PROJECT_NAME=your_project_name_here
export BASE_IMAGE_TAG=the_base_image_docker_tag_here
export IMAGE_TAG=your_desired_compile_container_docker_tag_here
export NEPTUNE_API_TOKEN=your_personal_neptune_api_token_here
export AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
```

or update your `.envrc` file accordingly.

### 2.2 Docker compose :whale:

The following `docker compose` services are typically associated with a project's `compile`
component:
- :construction: `compile`
- :warning: `compile-unit`
   - runs the `unit` test suite
- :warning: `compile-integration` (optional)
   - runs `integration` test suite (if applicable)
- :warning: `compile-functional` (optional)
   - runs `functional` test suite (if applicable)
- :rocket: `compile-download-model`
   - downloads the uncompilde model from the model registry
- :rocket: `compile-compile-model`
   - compiles the model
- :rocket: `compile-validate-model`
   -  validates the model compilation output
- :rocket: `compile-upload-model`
   - uploads the compiled model to the model registry


### 2.3 Building the `compile` component :construction:

To locally build the image
- using the `${BASE_IMAGE_TAG}` version of the base image, and
- using the `docker-compose.dev.yaml`,
- using the `development` build stage,
- tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-compile:${IMAGE_TAG}`, run
the `make` target:

```bash
make projects.build/${PROJECT_NAME} COMPONENT=compile
```

### 2.3 Example implementation :nut_and_bolt: :eyes:

For reference implementations of all below concepts, i.e.,
- `Dockerfile` structure
- `config` directory and `dotenv` configuration files
- `src` directory and source code layout
- `test` suite implementations
- `docker compose` files and services for `dev` and `ci`

see the
- [**`keywords` project's `compile` component directory**](../keywords/compile) and
- [**corresponding docker compose service entries**](https://github.com/AirPR/ml-mesh/blob/35d007edb24e90797a2b0bf357ca67a49bbf301d/projects/keywords/docker-compose.dev.yaml#L63).**

## 3 Testing the `compile` component :warning:

To validate every change on the component, test suites should be run using the
`docker-compose.dev.yaml` file. The following test suites are implemented:

- `unit` (mandatory)
- `integration` (optional)
- `functional` (optional)

### 3.1 Run `unit` tests :warning: :nut_and_bolt:

To run the `unit` tests for the `compile` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/${PROJECT_NAME} COMPONENT=compile
```

### 3.2 Run `integration` tests :warning: :nut_and_bolt: :nut_and_bolt:

To run the `integration` tests for the `compile` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/${PROJECT_NAME} COMPONENT=compile
```

### 3.3 Run `functional` tests :warning: :nut_and_bolt: :nut_and_bolt: :nut_and_bolt:

To run the `functional` tests for the `compile` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/${PROJECT_NAME} COMPONENT=compile
```

## 4 Running the `compile` component :rocket:

### 4.1 Without containers (initial development and debugging only)

For development purposes, the pipeline can be run locally without containers. Note that while this
could ease the development process, it has some downsides since you are now outside of your bespoke
container runtime environment. The following risks should be considered. It's important to test
the functionality of your code via make command once the development is finished.

- Some python & OS-level dependencies might be missing
- Some env vars might be missing

1. Change into the `projects/${PROJECT_NAME}/compile/src` directory
   - `cd projects/${PROJECT_NAME}/compile`
2. Running the below one after the other will export outputs to the local
   `projects/keywords/compile/src/outputs` directory:

- `python -m src.download_uncompiled_model`
- `python -m src.compile_model`
- `pytest src/test_compiled_model -ra -vvv --full-trace --tb=long --capture=no`
- `python -m src.upload_compiled_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 4.2 With containers (recommended approach) :rocket: :whale:

Running the below steps will create an additional `outputs` directory in the
`projects/${PROJECT_NAME}/compile` directory, holding all the below 4 steps' outputs in 4 separate
subdirectories for easier inspection & developing:

- `projects/${PROJECT_NAME}/compile/outputs/download`
- `projects/${PROJECT_NAME}/compile/outputs/compile`
- `projects/${PROJECT_NAME}/compile/outputs/validate`
- `projects/${PROJECT_NAME}/compile/outputs/upload`

To run the `compile` container locally as a pipeline using
- the services implemented in the `projects` `docker-compose.dev.yaml` file and
- internal `projects` level `make` & `docker compose` utilities,

follow the below steps.

#### 4.2.1 Update configuration

Update
- the `dev.env` file in the `config` directory and
- the `docker-compose.dev.yaml`'s `compile` service as needed. `docker compose` will inject the
file's environment variable values directly into the running container(s) (see below) to allow for
 pipeline runtime configurations without requiring a rebuild of the docker container.

The following environment variables in the `dev.env` file are responsible for enabling/disabling the
 execution of the associated pipeline step; all of them default to `false`. They are:

- `COMPILE_PIPELINE_EXECUTION_DOWNLOAD`
  - If `true`, pipeline will execute model download step
  - corresponding `make` target argument: `DOWNLOAD`
- `COMPILE_PIPELINE_EXECUTION_COMPILE`
  - If `true`, pipeline will execute model compilation step
  - corresponding `make` target argument: `COMPILE`
- `COMPILE_PIPELINE_EXECUTION_TEST`
  - If `true`, pipeline will execute compiled model test step
  - corresponding `make` target argument: `TEST`
- `COMPILE_PIPELINE_EXECUTION_UPLOAD`
  - If `true`, pipeline will execute compiled model upload step
  - corresponding `make` target argument: `UPLOAD`

Since they all default to `false`, we can run any one individual pipeline step by enabling the
step's associated `make` target argument as shown below.

#### 4.2.2 Download the model

```bash
make projects.run/${PROJECT_NAME} COMPONENT=compile TASK=download-model
```

#### 4.2.3 Compile the model

```bash
make projects.run/${PROJECT_NAME} COMPONENT=compile TASK=compile-model
```

#### 4.2.4 Validate compiled model:

```bash
make projects.run/${PROJECT_NAME} COMPONENT=compile TASK=validate-model
```

#### 4.2.5 Upload compiled model:

```bash
make projects.run/${PROJECT_NAME} COMPONENT=compile TASK=upload-model
```
