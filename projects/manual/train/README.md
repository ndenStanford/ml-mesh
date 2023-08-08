# `Train Manual`

Set PROJECT_NAME to "keywords", "ner", or "sentiment"

`export PROJECT_NAME=?`

## 1 Overview

The `${PROJECT_NAME}-train` container image provides the code and runtime environment for retrieving a
specified feature extraction pipeline from huggingface and registering it on our internal neptun AI
model registry.

The python module implementing the above process is `register_trained_model.py`.

It draws its configurations from the `settings.py` module, which parses all required
environment variable either

- from the environment, or, if not specified,
- from the `config/dev.env` dotenv file (locally or in the container when running inside docker)

Specs defined in the `config/prod.env` is used only during CI processes.

## 2 Running the pipeline

### 2.1 Without containers

For development purposes, the pipeline can be run locally without containers. Note that while this could ease the development process, it has some downsides since you are now outside of your bespoke container runtime environment. The following risks should be considered. It's important to test the functionality of your code via make command once the development is finished.

- Some dependencies might be missing
- Some env vars might be missing
- All potential dependency docker services (none in the case of train, but there will be some for compile for example) will have to be manually run

1. Set the neptune authentication token value
   - `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/${PROJECT_NAME}/train/src` directory
   - `cd projects/${PROJECT_NAME}/train`
3. Run the model retrieval + registering step
   - `python -m src.register_trained_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 2.2 With containers

#### 2.2.1 Building the docker container

To locally build the image tagged as
`063759612765.dkr.ecr.us-east-1.amazonaws.com/${PROJECT_NAME}-train:latest`, run the `make` target:

```make
make projects.build/${PROJECT_NAME} \
  COMPONENT=train \
  ENVIRONMENT=dev
```
You can replace `latest` with `$IMAGE_TAG` if you would prefer to tag with a different name. Make sure you've exported a value for `$IMAGE_TAG`

#### 2.2.2 Running the components inside docker

1. Export run environment variables

   - `export NEPTUNE_API_TOKEN=?`
   - `export PATH_TO_REPOSITORY=?`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the container:

You can run the command with this command (which uses docker compose):

```
make projects.start/${PROJECT_NAME} COMPONENT=train
```

If you're using a different tag e.g. `$IMAGE_TAG`, make sure to replace `latest` with it.