#  Onclusive ML Mesh

This repo contains the codebase for the machine learning APIs service mesh.

## Project organisation

This project contains the modular implementation of the logic powering Onclusive's ML stack:

### Repository philosophy

ML projects are decomposed into multiple pre-defined steps that represent an abstraction of a model
lifecycle at Onclusive.

- **ingest**: if the data needed for training is external to Onclusive, an ingest step is needed to bring data into our internal storage.
- **prepare**: dataset pre-processing and feature engineering (if any).
- **train**: model training.
- **compile**: model compilation (it can be so that the model runs on a specific architecture of a model quantization);
- **serve**: model served as a REST API.
- **show**: UI component with streamlit.

Strict abstraction boundaries help express the invariant and logical consistency of each component behaviour (input, processing and output).
This allows us to create well defined patterns that can be applied specifically to implement each of these steps on new projects.
Not all of these steps are mandatory: for instance, pre-trained model used for zero-shot learning will not have a prepare and train step.

## Developing

### Setting up your local environment

If you are on MacOS, you can run the script `./bin/boostrap/darwin` that will set up your local machine for development. If you are using Linux, the next section describes the installation steps.

**Windows and Linux setup is not supported yet - to be explored**. If you want to contribute to this please reach out to the MLOPs team.

### Manual installation

In order to setup your local development enviroment, please follow these steps:

- [ ] Install core dependencies
- [ ] Setup your AWS config
- [ ] Install poetry
- [ ] Setup your python environment
- [ ] Install git hooks (optional)

### Contributing to the codebase

#### Creating a new core docker image

In order to add a new core docker image, open a new [issue](./.github/ISSUE_TEMPLATE/06_NEW_CORE_DOCKER_IMAGE.md) and follow the steps outlined in the checklist.

#### Creating a new library

In order to add a new library, open a new [issue](./.github/ISSUE_TEMPLATE/05_NEW_LIB.md) and follow the steps outlined in the checklist.

#### Creating a new project

In order to add a new project, open a new [issue](./.github/ISSUE_TEMPLATE/03_NEW_PROJECT.md) and follow the steps outlined in the checklist.

#### Updating an existing project

In order to add a new component to an existing project, open a new [issue](./.github/ISSUE_TEMPLATE/04_NEW_PROJECT_COMPONENT.md) and follow the steps outlined in the checklist.

## Dependency management

Python is our language of choice. In order to manage versions effectively, we recommend to use [pyenv](https://github.com/pyenv/pyenv). In order to setup your environment with the repository official version.

### Common issues

#### Poetry command takes longer to run

If poetry commands take longer to run, it's a good idea to clear the pypi cache:

```bash
poetry cache clear pypi --all
```

#### Docker-compose tries to download images instead of building (MacOS)

The error message is:

```text
Failed to solve with frontend dockerfile.v0: failed to create LLB definition: pull access denied, repository does not exist or may require authorization: server message: insufficient_scope:
authorization failed
```

Run the following command:

```shell
export DOCKER_BUILDKIT=0
```

## Resources

- [Poetry](https://python-poetry.org/docs/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Make](https://www.gnu.org/software/make/manual/make.html)
- [Python versions status](https://devguide.python.org/versions/)
