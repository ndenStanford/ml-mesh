# `keywords-train`

## 1 Overview

The `keywords-train` container image provides the code and runtime environment for retrieving a
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

For development purposes, the pipeline can be run locally without containers.

1. Set the neptune authentication token value
   - `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/keywords/train/src` directory
   - `cd projects/keywords/train`
3. Run the model retrieval + registering step
   - `python -m src.register_trained_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 2.2 With containers

#### 2.2.1 Building the docker container

To locally build the image tagged as
`063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:latest`, run the `make` target:

```make
make projects.build/keywords \
  COMPONENT=train \
  ENVIRONMENT=dev
```

#### 2.2.2 Running the components inside docker

1. Export run environment variables

   - `export NEPTUNE_API_TOKEN=?`
   - `export PATH_TO_REPOSITORY=?`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the container:

```docker
docker run \
  --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
  --env-file $PATH_TO_REPOSITORY/projects/keywords/train/config/dev.env \
  -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:latest \
  python -m src.register_trained_model
```

- Note: If the `--env-file` command is omitted in the above steps,
  the pipeline will fall back on the default values defined in the `settings.py` file.
