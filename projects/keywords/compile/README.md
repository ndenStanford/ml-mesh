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
  ENVIRONMENT=dev \
  IMAGE_TAG="some-tag"
```

#### 2.2.2 Running the components inside containers using `make` and `docker compose`

Running the below steps will create an additional `outputs` directory in the
`projects/keywords/compile` directory, holding all the below 4 steps' outputs in 4 separate
subdirectories for easier inspection & developing:

- `projects/keywords/compile/outputs/download`
- `projects/keywords/compile/outputs/compile`
- `projects/keywords/compile/outputs/validate`
- `projects/keywords/compile/outputs/upload`

To run the pipeline locally using the configurations in the `docker-compose.dev.yaml` file and internal `projects` level `make` utilities, follow the below steps.

1. Ensure the following variables are exported in your CLI:

   - `NEPTUNE_API_TOKEN`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the pipeline

- Download the uncompiled model:

  ```docker
  make projects.compile/keywords \
            ENVIRONMENT=dev \
            PIPELINE_COMPONENT=download-model \
            IMAGE_TAG="some-tag" # whichever keywords-compile image tag you want to run
  ```

- Compile the model:

  ```docker
  make projects.compile/keywords \
            ENVIRONMENT=dev \
            PIPELINE_COMPONENT=compile-model \
            IMAGE_TAG="some-tag"
  ```

- Test compiled model:

  ```docker
  make projects.compile/keywords \
            ENVIRONMENT=dev \
            PIPELINE_COMPONENT=validate-model \
            IMAGE_TAG="some-tag"
  ```

- Upload compiled model:

  ```docker
  make projects.compile/keywords \
            ENVIRONMENT=dev \
            PIPELINE_COMPONENT=upload-model \
            IMAGE_TAG="some-tag"
  ```

  - Note: If the `--env-file` command is omitted in the above steps,
    the pipeline will fall back on the default values defined in the `settings.py` file.
  - Note: The `volume` mount command `--mount type=volume,source=...` will create a docker volume
    named `keywords_compile-pipeline-vol` on your machine. Follow the docker docs to remove it to unblock repeated
    downloads when re-running the first component

### 2.3 With Github Actions

Two custom workflows have been created to orchestrate the neuron compilation on a customized, self
hosted `inf1.x` Github Actions runner.

- the model compilation workflow `.github/workflows/_compile_model.yaml` oversees the model
  compilation by provisioning the runner as needed, and running the 4 pipeline components described
  in the previous 2 sections.
- the customized runner provisioning workflow `.github/workflows/_provision_customized_runner.yaml`
  that provisions a specified EC2 instance as a self hosted runner and installs `neuron` runtimes
  and/or `docker-compose` as needed

dummy change to trigger keywords-compile build again
