#  Onclusive ML Mesh

This repo contains the codebase for the machine learning APIs service mesh.

## Repository organisation

This repository contains the modular implementation of the logic powering Onclusive's ML stack:
1. [internal libraries](./libs)
2. [internally maintained core images](./docker)
3. [applications serving **internally** maintained models](./projects)
4. [applications serving **externally** maintained models](./apps)

### Libraries

A top-level doc on can be found [here](./libs/README.md)

All internal libraries can be found [here](./libs). See individual library for  detailed
documentation.

### Core images

An overview of developer utilitites and existing images on can be found [here](./docker/README.md)

All internal core images can be found [here](./docker). See individual core image for detailed
documentation.

### Projects

ML projects are decomposed into multiple pre-defined steps that represent an abstraction of a model
lifecycle at Onclusive.

An overview of developer utilitites and existing images on can be found [here](./projects/README.md)

- **ingest**: if the data needed for training is external to Onclusive, an ingest step is needed to
bring data into our internal storage.
- **register**: register features to be used in training component.
  - [see here](./projects/docs/00_register.md) for this component's doc
- **train**: model training and registering to internal model registry.
  - [see here](./projects/docs/01_train.md) for this component's doc
- **compile**: model compilation (optimized for serving) and registering to internal model registry
  - [see here](./projects/docs/02_compile.md) for this component's doc
- **serve**: model served as a REST API.
  - [see here](./projects/docs/03_serve.md) for this component's doc

Strict abstraction boundaries help express the invariant and logical consistency of each component
behaviour (input, processing and output). This allows us to create well defined patterns that can
 be applied specifically to implement each of these steps on new projects. Not all of these steps
 are mandatory: for instance, pre-trained model used for zero-shot learning will not have a prepare
 and train step.

### Apps

An overview of developer utilitites and existing images on can be found [here](./apps/README.md)

All internal core images can be found [here](./apps/). See individual app for detailed
documentation.

## Developing

### Setting up your local environment

If you are on MacOS, you can run the script `./bin/boostrap/darwin` that will set up your local machine for development. If you are using Linux, use `./bin/boostrap/linux`.

**Windows setup is not supported yet - to be explored**. If you want to contribute to this please reach out to the MLOPs team.

#### Setup AWS credentials

Setup your aws credentials for dev and prod ML accounts (Default region name  should be us-east-1 and Default output format should be JSON). Ask @mlops on slack to get your credentials created if you
don't have them already.

For your dev credentials:

```shell
aws configure --profile dev
```

For your prod credentials:

```shell
aws configure --profile prod
```

You can also switch profiles at any time by updating the environment variable as follows

```shell
export AWS_PROFILE=dev
```

#### Build all base images

As all images used in projects and apps are based on our core docker images. It helps save time to build all images. Run the command

```shell
make docker.build/python-base
make docker.build/fastapi-serve
make docker.build/neuron-compile
make docker.build/neuron-inference
```

It takes about 10 minutes to run, go stretch your legs, get a coffee, or consult our [Contribution Guide](https://onclusive.atlassian.net/l/cp/u1Mz7m6M).

### Contributing to the codebase

[See here for a detailed step-by-step guide on how to contribute to the mesh](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3241050137/ml-mesh).

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

#### No space left on disk (remote instance)

If you run into this error, you can use the make command:

```
make clean
```

## Resources

- [Poetry](https://python-poetry.org/docs/)
- [Pyenv](https://github.com/pyenv/pyenv)
- [Make](https://www.gnu.org/software/make/manual/make.html)
- [Python versions status](https://devguide.python.org/versions/)
