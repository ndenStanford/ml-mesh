#  Onclusive ML Mesh

This repo contains the codebase for the machine learning APIs service mesh.

## Project organisation

This project contains the modular implementation of the logic powering Onclusive's ML stack:

### Repository philosophy

ML projects are decomposed into multiple pre-defined steps that represent an abstraction of a model
lifecycle at Onclusive.

- **prepare**: dataset pre-processing and feature engineering (if any).
- **train**: model training.
- **compile**: model compilation (it can be so that the model runs on a specific architecture of a model quantization);
- **serve**: model served as a REST API.
- **backfill**: data enriched with a previous version of the model is re-enriched with a newer version.
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
- [ ] Setup your python environment
- [ ] Install git hooks (optional)

### Contributing to the codebase

#### Creating a new core docker image

#### Updating an existing core docker image

#### Creating a new library

#### Updating an existing library

#### Creating a new project

#### Updating an existing project

## Dependency management

Python is our language of choice. In order to manage versions effectively, we recommend to use [pyenv](https://github.com/pyenv/pyenv). In order to setup your environment with the repository official version.

### Note

If poetry commands take longer to run, it's a good idea to clear the pypi cache:

```bash
poetry cache clear pypi --all
```

## Running unit tests

WIP.

## Upgrading python version

## Resources

- [Poetry](https://python-poetry.org/docs/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Make](https://www.gnu.org/software/make/manual/make.html)
- [Python versions status](https://devguide.python.org/versions/)
