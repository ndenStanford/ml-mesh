# The `compile` component

This document outlines how to run and test your project's `compile` component.

## 1 Scope of the `compile` component

### 1.1 Overview

The `${PROJECT_NAME}-compile` container image provides the code and runtime environment for
- retrieving a specified, uncompiled model / pipeline from the neptune AI model registry,
- compiling it to a format optimized for serving (e.g. neuron)
- validating the compiled model / pipeline via regression tests
- registering the compiled model / pipeline on our internal neptune AI model registry.

Each of the 4 steps corresponds to a (set of) python module(s):

1. `download_uncompiled_model.py`
2. `compile_model.py`
3. Regression test suite inside `test_compiled_model` directory:
   - `pytest.ini`
   - `conftest.py`
   - `compiled_model_test.py`
4. `upload_compiled_model.py`

Each component draws its configurations from the `settings.py` module, which parses all required
environment variable either

- from the environment, or, if not specified,
- from the `config/dev.env` dotenv file (locally or in the container when running inside docker)

Specs defined in the `config/prod.env` is used only during CI processes.

Orchestration of these components into the model compile pipeline is done by Github Actions of this
same `ml-mesh` repository (as opposed to all other orchestration happening in `ml-platform`)

### 1.2 Setup & references

Projects implementing a `train` component are
- `keywords`
- `ner`
- `sentiment`

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

**see the [`keywords` project's `compile` component directory](https://github.com/AirPR/ml-mesh/tree/develop/projects/keywords/train) and [corresponding docker compose service entries](https://github.com/AirPR/ml-mesh/blob/35d007edb24e90797a2b0bf357ca67a49bbf301d/projects/keywords/docker-compose.dev.yaml#L63).**


## 2 Running the `compile` component

### 2.1 Without containers (initial development and debugging only)

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

### 2.2 With containers (recommended approach)

#### 2.2.1 Building the docker container

To locally build the image
- using the ${BASE_IMAGE_TAG} version of the base image, and
- tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-copmile:${IMAGE_TAG}`, run
the `make` target:

```bash
make projects.build/${PROJECT_NAME} \
  COMPONENT=compile \
  ENVIRONMENT=dev \
  BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
  IMAGE_TAG=${IMAGE_TAG}
```

#### 2.2.2 Running the docker container using docker compose

Running the below steps will create an additional `outputs` directory in the
`projects/${PROJECT_NAME}/compile` directory, holding all the below 4 steps' outputs in 4 separate
subdirectories for easier inspection & developing:

- `projects/${PROJECT_NAME}/compile/outputs/download`
- `projects/${PROJECT_NAME}/compile/outputs/compile`
- `projects/${PROJECT_NAME}/compile/outputs/validate`
- `projects/${PROJECT_NAME}/compile/outputs/upload`

To run the `compile` container locally as a pipeline using
- the services implemented in the `projects` `docker-compose.dev.yaml` file and
- internal `projects` level `make` & `docker compose` utilities, follow the below steps.

1. Update the `dev.env` file in the `config` directory as needed. `docker compose` will inject the
   file's environment variable values directly into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the pipeline

- Download the uncompiled model:

  ```bash
  make projects.compile/${PROJECT_NAME} \
   ENVIRONMENT=dev \
   PIPELINE_COMPONENT=download-model \
   IMAGE_TAG=${IMAGE_TAG}
  ```

- Compile the model:

  ```bash
  make projects.compile/${PROJECT_NAME} \
   ENVIRONMENT=dev \
   PIPELINE_COMPONENT=compile-model \
   IMAGE_TAG=${IMAGE_TAG}
  ```

- Test compiled model:

  ```bash
  make projects.compile/${PROJECT_NAME} \
   ENVIRONMENT=dev \
   PIPELINE_COMPONENT=validate-model \
   IMAGE_TAG=${IMAGE_TAG}
  ```

- Upload compiled model:

  ```bash
  make projects.compile/${PROJECT_NAME} \
   ENVIRONMENT=dev \
   PIPELINE_COMPONENT=upload-model \
   IMAGE_TAG=${IMAGE_TAG}
  ```

  - Note: If the `--env-file` command is omitted in the above steps,
    the pipeline will fall back on the default values defined in the `settings.py` file.
  - Note: The `volume` mount command `--mount type=volume,source=...` will create a docker volume
    named `keywords_compile-pipeline-vol` on your machine. Follow the docker docs to remove it to unblock repeated downloads when re-running the first component

## 3 Testing the training component

To validate every change on the component, test suites should be run using the
`docker-compose.dev.yaml` file. The following test suites are implemented:

- `unit` (mandatory)
- `integration` (optional)
- `functional` (optional)

### 2.1 Run `unit` tests

To run the `unit` tests for the `compile` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/${PROJECT_NAME} COMPONENT=compile ENVIRONMENT=dev
```

### 2.2 Run `integration` tests

To run the `integration` tests for the `compile` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/${PROJECT_NAME} COMPONENT=compile ENVIRONMENT=dev
```

### 2.3 Run `functional` tests

To run the `functional` tests for the `compile` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/${PROJECT_NAME} COMPONENT=compile ENVIRONMENT=dev
```
