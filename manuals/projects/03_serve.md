# The `serve` component

This document outlines how to run and test your project's `serve` component.

## 1 Scope of the `serve` component

### 1.1 Overview

The `${PROJECT_NAME}-serve` container image provides the code and runtime environment for
- downloading a model registered on the neptune AI model registry (if applicable - see below)
- serving a model **owned & maintained internally** by the ML team
- uploading test results to the neptune AI model registry (if applicable - see above)

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
```

For reference implementations of all below concepts, i.e.,
- `Dockerfile` structure
- `config` directory and `dotenv` configuration files
- `src` directory and source code layout
- `test` suite implementations
- `docker compose` files and services for `dev` and `ci`

**see the `keywords` project.**


## 2 Running the training component

### 2.1 Without containers (initial development and debugging only)

For development purposes, the pipeline can be run locally without containers. Note that while this
could ease the development process, it has some downsides since you are now outside of your bespoke
container runtime environment. The following risks should be considered. It's important to test
the functionality of your code via make command once the development is finished.

- Some python & OS-level dependencies might be missing
- Some env vars might be missing

1. Set the neptune authentication token value
   - `export NEPTUNE_API_TOKEN==your_personal_neptune_api_token_here`
2. Change into the `projects/${PROJECT_NAME}/train/src` directory
   - `cd projects/${PROJECT_NAME}/train`
3. Run the model retrieval + registering step
   - `python -m src.register_trained_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 2.2 With containers (recommended approach)

#### 2.2.1 Building the docker container

To locally build the image tagged as
`063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-train:latest`, run the `make` target:

```bash
make projects.build/${PROJECT_NAME} \
  COMPONENT=train \
  ENVIRONMENT=dev
```
You can replace `latest` with `$IMAGE_TAG` if you would prefer to tag with a different name. Make
sure you've exported a value for `$IMAGE_TAG`

#### 2.2.2 Running the components inside docker

1. Export run environment variables

   - `export NEPTUNE_API_TOKEN=?`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the container:

You can run the command with this command (which uses docker compose):

```
make projects.start/${PROJECT_NAME} COMPONENT=train
```

If you're using a different tag e.g. `$IMAGE_TAG`, make sure to replace `latest` with it.

## 3 Testing the training component

To validate every change on the component, test suites should be run using the `docker-compose.dev.yaml` file.
The following test suites are implemented:

- `unit` (mandatory)
- `integration` (optional)
- `functional` (optional)

### 2.1 Run `unit` tests

To run the `unit` tests for the `train` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/${PROJECT_NAME} COMPONENT=train ENVIRONMENT=dev
```

### 2.2 Run `integration` tests

To run the `integration` tests for the `train` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/${PROJECT_NAME} COMPONENT=train ENVIRONMENT=dev
```

### 2.3 Run `functional` tests

To run the `functional` tests for the `train` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/${PROJECT_NAME} COMPONENT=train ENVIRONMENT=dev
```
