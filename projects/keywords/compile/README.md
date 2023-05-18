# `keywords-compile`

## 1 Overview

The `keywords-compile` container image provides the runtime environment for all 4 components of the
**model compilation** segment of
[the CI pipeline outlined in this RFC](https://onclusive01-my.sharepoint.com/:w:/g/personal/sebastian_scherer_onclusive_com/EXMw2nQrwSpBn4uKzY90Hb4BBFq1NHsYByDAo9-uc83iLg?e=B9ULGd):

1. download uncompiled model (either `base` or `trained`)
2. compile model (either `generic` or `neuron` torchscript tracing)
3. validate compiled model
4. registering compiled model on neptune AI

Each of the 4 components corresponds to a (set of) python module(s):

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

## 2 Running the pipeline

### 2.1 Without containers

For development purposes, the pipeline can be run locally without containers.

1. Set the neptune authentication token value
   - `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/keywords/compile` directory
   - `cd projects/keywords/compile`
3. Running the below one after the other will export outputs to the local
   `projects/keywords/compile/src/outputs` directory:

- `python -m src.download_uncompiled_model`
- `python -m src.compile_model`
- `pytest src/test_compiled_model -ra -vvv --full-trace --tb=long --capture=no`
- `python -m src.upload_compiled_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 2.2 With containers

#### 2.2.1 Building the docker container

To locally build the image tagged as
`063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-compile:latest`, run the `make` target:

```make
make projects.build/keywords \
  COMPONENT=compile \
  ENVIRONMENT=dev
```

#### 2.2.2 Running the components inside docker

1. Export run environment variables:

   - `export CONTAINER_VOLUME_DIR=?`
   - `export NEPTUNE_API_TOKEN=?`
   - `export PATH_TO_REPOSITORY=?`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the pipeline

- Download the uncompiled model:

  ````docker
  docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    --env IO_OUTPATH=$CONTAINER_VOLUME_DIR \
    --env-file $PATH_TO_REPOSITORY/projects/keywords/compile/config/dev.env \
    --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
    -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-compile:latest \
    python -m src.download_uncompiled_model```
  ````

- Compile the model:

  ```docker
  docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    --env IO_OUTPATH=$CONTAINER_VOLUME_DIR \
    --env-file $PATH_TO_REPOSITORY/projects/keywords/compile/config/dev.env \
    --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
    --device /dev/neuron0 \
    -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-compile:latest \
    python -m src.compile_model
  ```

- Test compiled model:

  ```docker
  docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    --env IO_OUTPATH=$CONTAINER_VOLUME_DIR \
    --env-file $PATH_TO_REPOSITORY/projects/keywords/compile/config/dev.env \
    --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
    --device /dev/neuron0 \
    -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-compile:latest \
    pytest src/test_compiled_model -ra -vvv --full-trace --tb=long --capture=no
  ```

- Upload compiled model:

  ```docker
  docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    --env IO_OUTPATH=$CONTAINER_VOLUME_DIR \
    --env-file $PATH_TO_REPOSITORY/projects/keywords/compile/config/dev.env \
    --mount type=volume,source=workflow-volume,target=$CONTAINER_VOLUME_DIR \
    -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/keywords-compile:latest \
    python -m src.upload_compiled_model
  ```

  - Note: If the `--env-file` command is omitted in the above steps,
    the pipeline will fall back on the default values defined in the `settings.py` file.
  - Note: The `volume` mount command `--mount type=volume,source=...` will create a docker volume
    named `workflow-volume` on your machine. Follow the docker docs to remove it to unblock repeated
    downloads when re-running the first component
