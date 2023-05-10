# `keywords-train`

## 1 Overview

The `keywords-train` container image provides the code and runtime environment for retrieving a
specified feature extraction pipeline from huggingface and registering it on our internal neptun AI model registry.

The python module implementing the above process is `register_trained_model.py`.

It draws its configurations from the `settings.py` module, which in turn expects one of the two
`.dotenv` files to be present in the `src/config` subdirectory (locally or in the container when running inside docker):

- `.dev`
- `.prod`

## 2 Running the pipeline

### 2.1 Without containers

For development purposes, the pipeline can be run locally without containers.

1. Set the neptune authentication token value: `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/keywords/train/src` directory: `cd projects/keywords/train/src`
3. Run the model retrieval + registering step: `python -m src.register_trained_model`

By default, the `settings.py` script will draw its environment variable values from the `.dev` file
located in `src/config`. Editing that file allows for configuring development pipeline runs.

### 2.2 With containers

#### 2.2.1 Building the docker container

To locally build the image tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:latest`, run the `make` target:

```make
make projects.build/keywords \
  COMPONENT=train \
  ENVIRONMENT=dev
```

#### 2.2.2 Running the components inside docker

1. Export run environment variables

   - `export NEPTUNE_API_TOKEN=?`
   - `export PATH_TO_REPOSITORY=?`

2. Update the `.dev` file in the `src/config` directory as needed. We will mount it into the running
   containers (See below) to allow for pipeline runtime configurations without requiring a rebuild of the docker container.
3. Run the container:

```docker
docker run \
  --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
  --mount type=bind,source=$PATH_TO_REPOSITORY/projects/keywords/train/src/config/,target=/projects/keywords/train/src/config,readonly \
  -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-train:latest \
  python -m src.register_trained_model
```

- Note: If the `bind` mount command `--mount type=bind,source=...` is omitted in the below steps, the pipeline will fall back on the file `.dev` file that was copied into the image at build time.
