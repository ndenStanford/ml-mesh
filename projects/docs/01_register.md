# The `register` component

This document outlines how to run and test your project's `register` component.

## 1 Scope of the `register` component :mag_right:

### 1.1 Overview :mount_fuji:

A project's `register` container image provides the code and runtime environment for declaring the features to be used in a project's `train` component.

The python module implementing the above process is `src/register_features.py`.

It draws its configurations from the `src/settings.py` module, which parses all required
environment variable either

- from the environment, or, if not specified,
- from the `config/dev.env` dotenv file (locally or in the container when running inside docker)

Specs defined in the `config/prod.env` are used only during CI processes.

## 2 Setup & references :wrench:

Projects implementing a `register` component are
- **`iptc`** :key::memo:

### 2.1 Environment variables :deciduous_tree:

To follow the instructions in this guide, run

```bash
export PROJECT_NAME=your_project_name_here
export BASE_IMAGE_TAG=the_base_image_docker_tag_here
export IMAGE_TAG=your_desired_register_container_docker_tag_here
export AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
export AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
```

or update your `.envrc` file accordingly.

### 2.2 Docker compose :whale:

The following `docker compose` services are typically associated with a project's `register` component:
- `register`
   - contains build section of feature-registration image
   - contains the container run command to execute feature-registration
- `register-unit`
   - used to run `unit` test suite

### 2.3 Building the `register` component :construction:

To locally build the image
- using the `${BASE_IMAGE_TAG}` version of the base image, and
- using the `docker-compose.dev.yaml`,
- using the `development` build stage,
- tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-register:${IMAGE_TAG}`,

run:

```bash
make projects.build/${PROJECT_NAME} COMPONENT=register
```

### 2.4 Example implementation :nut_and_bolt: :eyes:

For reference implementations of all below concepts, i.e.,
- `Dockerfile` structure
- `config` directory and `dotenv` configuration files
- `src` directory and source code layout
- `test` suite implementations
- `docker compose` files and services for `dev` and `ci`

see the
- [**`iptc` project's `register` component**](../iptc/register) and
- [**corresponding docker compose service entries**](../iptc/register/docker-compose.dev.yaml).

## 3 Testing the `register` component :warning:

To validate every change on the component, test suites should be run using the `docker-compose.dev.yaml` file.
The following test suites are implemented:

- `unit` (mandatory)
- `integration` (optional)
- `functional` (optional)

### 3.1 Run `unit` tests :warning: :nut_and_bolt:

To run the `unit` tests for the `register` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.unit/${PROJECT_NAME} COMPONENT=register
```

### 3.2 Run `integration` tests :warning: :nut_and_bolt: :nut_and_bolt:

To run the `integration` tests for the `register` component using the `docker-compose.dev.yaml` file, run:

```bash
make projects.integration/${PROJECT_NAME} COMPONENT=register
```

### 3.3 Run `functional` tests :warning: :nut_and_bolt: :nut_and_bolt: :nut_and_bolt:

To run the `functional` tests for the `register` component using the `docker-compose.dev.yaml` file,  run:

```bash
make projects.functional/${PROJECT_NAME} COMPONENT=register
```


## 4 Running the `register` component :rocket:

### 4.1 Without containers (initial development and debugging only)

For development purposes, the pipeline can be run locally without containers. Note that while this
could ease the development process, it has some downsides since you are now outside of your bespoke
container runtime environment. The following risks should be considered. It's important to test
the functionality of your code via make command once the development is finished.

- Some python & OS-level dependencies might be missing
- Some env vars might be missing

1. Change into the `projects/${PROJECT_NAME}/register/src` directory
   - `cd projects/${PROJECT_NAME}/register`
2. Run the feature-registration step
   - `python -m src.register_features`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 4.2 With containers (recommended approach) :rocket: :whale:

To run the `register` container locally as a one-step pipeline using
- the services implemented in the `projects` `docker-compose.dev.yaml` file and
- internal `projects` level `make` & `docker compose` utilities,

follow the below steps.

#### 4.2.1 Update configuration

Update
- the `dev.env` file in the `config` directory and
- the `docker-compose.dev.yaml`'s `register` service
 as needed. `docker compose` will inject the file's environment variable values directly into the
 running container (see below) to allow for pipeline runtime configurations without requiring a
 rebuild of the docker container.

#### 4.2.2 register the features

```bash
make projects.start/${PROJECT_NAME} COMPONENT=register
```
