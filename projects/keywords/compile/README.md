# 1 Overview

The `keywords-compile` container image provides the runtime environment for all 4 components of the
**model compilation** segment of [the CI pipeline outlined in this RFC](https://onclusive01-my.sharepoint.com/:w:/g/personal/sebastian_scherer_onclusive_com/EXMw2nQrwSpBn4uKzY90Hb4BBFq1NHsYByDAo9-uc83iLg?e=B9ULGd):

1. download uncompiled model (either `base` or `trained`)
2. compile model (either `generic` or `neuron` torchscript tracing)
3. validate compiled model
4. registering compiled model on neptune AI

Each of the 4 components corresponds to a python module:

1. `download_uncompiled_model.py`
2. `compile_model.py`
3. `validate_compiled_model.py`
4. `upload_compiled_model.py`

Each module draws its configurations from the `settings.py` module, which in turn expects one of the two `.dotenv` files to be present in the `src/config` subdirectory (locally or in the container when running inside docker):

- `.dev`
- `.prod`

Orchestration of these components into the model compile pipeline is done by Github Actions of this same `ml-mesh` repository (as opposed to all other orchestration happening in `ml-platform`). The [modeol compile workflow can be found here](#add-link-here)

# 2 Running the pipeline

## 2.1 Without containers

For development purposes, the pipeline can be run locally without containers.

1. Set the neptune authentication token value: `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/keywords/compile/src` directory: `cd projects/keywords/compile/src`
3. Running the below one after the other will export outputs to the local `projects/keywords/compile/src/outputs` directory:
  - `python -m src.download_uncompiled_model`
  - `python -m src.compile_model`
  - `pytest src.compiled_model_test.py -ra -vvv --full-trace --tb=long --capture=no`
  - `python -m src.upload_compiled_model`

By default, the `settings.py` script will draw its environment variable values from the `.dev` file located in `src/config`. Editing that file allows for configuring development pipeline runs.

## 2.2 With containers

### 2.2.1 Building the docker container

1. Export build environment variables
  - `export OWNER=?`
  - export `IMAGE_TAG=?`
2. Run the `make` target: `make projects.build/keywords COMPONENT=compile OWNER=$OWNER IMAGE_TAG=$IMAGE_TAG TARGET_BUILD_STAGE=production`

### 2.2.2 Running the components inside docker

1. Export run environment variables
  - `export CONTAINER_VOLUME_DIR=/projects/keywords/compile/outputs`
  - `export NEPTUNE_API_TOKEN=?`
  - `export PATH_TO_REPOSITORY=?`

2. Update the `.dev` file in the `src/config` directory as needed. We will mount it into the running containers (See below) to allow for pipeline runtime configurations without requiring a rebuild of the docker container.
3. Run the pipeline
  - Download the uncompiled model:
    ```docker
    docker run \
      --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
      --env OUTPATH=$CONTAINER_VOLUME_DIR \
      --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
      --mount type=bind,source=$PATH_TO_REPOSITORY/projects/keywords/compile/src/config/,target=/projects/keywords/compile/src/config,readonly \
      --device /dev/neuron0 \
      -t $OWNER/keywords-compile:$IMAGE_TAG \
      python -m src.download_uncompiled_model```
  - Compile the model:
    ```docker
    docker run \
      --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
      --env OUTPATH=$CONTAINER_VOLUME_DIR \
      --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
      --mount type=bind,source=$PATH_TO_REPOSITORY/projects/keywords/compile/src/config/,target=/projects/keywords/compile/src/config,readonly \
      --device /dev/neuron0 \
      -t $OWNER/keywords-compile:$IMAGE_TAG \
      python -m src.compile_model
    ```
  - Test compiled model:
    ```docker
    docker run \
      --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
      --env OUTPATH=$CONTAINER_VOLUME_DIR \
      --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
      --mount type=bind,source=$PATH_TO_REPOSITORY/projects/keywords/compile/src/config/,target=/projects/keywords/compile/src/config,readonly \
      --device /dev/neuron0 \
      -t $OWNER/keywords-compile:$IMAGE_TAG \
      pytest src/compiled_model_test.py -ra -vvv --full-trace --tb=long --capture=no
    ```
  - Upload compiled model:
    ```docker
    docker run \
      --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
      --env OUTPATH=$CONTAINER_VOLUME_DIR \
      --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
      --mount type=bind,source=$PATH_TO_REPOSITORY/projects/keywords/compile/src/config/,target=/projects/keywords/compile/src/config,readonly \
      --device /dev/neuron0 \
      -t $OWNER/keywords-compile:$IMAGE_TAG \
      python -m src.upload_compiled_model
    ```
    - Note: If the `bind` mount command `--mount type=bind,source=...` is omitted in the below steps, the pipeline will fall back on the file `.dev` file that was copied into the image at build time.
    - Note: The `volume` mount command `--mount type=volume,source=...` will create a docker volume named `workflow-volume` on your machine. Follow the docker docs to remove it to unblock repeated downloads when re-running the first component
