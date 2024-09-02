# Core docker images

Core docker images are the base images used to power our projects and development environments.

## Images

Images are provided as a way to have a tight dependency management control from development to
production. Often, Deep learning libraries rely on low level components that can be unstable to
manage from one version to another. Moreover, any breaking changes in any of our dependencies
should be caught early on.


| Reference                | Base Image Reference        | Description                                            | Target Hardware | Validate |
| ------------------------ | ----------------------------| ------------------------------------------------------ | --------------- | -------- |
| `python-base`            | n/a                         | Python base for core and project components            | cpu             |          |
| `gpu-base`               | `nvidia/cuda` (external)    | Flexible GPU base (w/o torch)                          | gpu             |     x    |
| `gpu-train`              | `python-base`               | GPU base for project train components (w/ torch & hf)  | gpu             |     x    |
| `neuron-inference`         | `python-base`               | Neuron base for project compile components             | inf1            |     x    |
| `neuron-inference`       | `python-base`               | Neuron base for neuron inference-only components       | inf1            |     x    |
| `fastapi-serve`          | `python-base`               | Serving base for project serve components              | cpu             |          |
| `kubeflow-jupyter`       | `python-base`               | Kubeflow base for jupyter                              | cpu             |          |
| `kubeflow-torch-cpu`     | `kubeflow-jupyter`          | Kubeflow flavour of flexible pytorch (CPU) image       | cpu             |          |
| `kubeflow-torch-gpu`     | `gpu-base`                  | Kubeflow image for torch (GPU available)               | gpu             |          |
| `kubeflow-torch-inf`     | `python-base`               | Kubeflow image for torch (Inferentia available)        | inf1            |          |
| `kubeflow-data-science`  | `kubeflow-torch-cpu`        | DS image for kubeflow                                  | cpu             |          |
| `dask-base`              | `dask` (external)           | Kubeflow base for Dask Schedulers and Workers          | cpu             |          |

## Dependency management

These images share the same base, and python dependencies are managed in a way that they are tightly
 coupled from one environment to another.

All images that require a `pip-install` have dependencies manged via dependabot and updated every
month.


## Makefile Targets & Docker-Compose Services

We use a set of `make` targets to consistently call `docker compose` services declared in
- the [docker level development `docker-compose.dev.yaml`](./docker-compose.dev.yaml) and
- the [docker level CI `docker-compose.ci.yaml`](./docker-compose.ci.yaml)

files, respectively.

Available targets are:

```text

    docker.lock/<image>                     (Re-)writes poetry lock file of a core image (if exists). Variable(s): ENVIRONMENT.
    docker.build/<image>                    Builds the docker image. Variable(s): ENVIRONMENT.
    docker.login                            Logs into AWS ECR using credentials provided during AWS login
    docker.deploy/<image>                   Deploys docker image to ECR. Variable(s): ENVIRONMENT.
    docker.start/<image>                    Start development container for component. Variable(s): ENVIRONMENT.
    docker.stop/<image>                     Stop development container for component. Variable(s): ENVIRONMENT.
    docker.validate/<image>                 Runs image test suite (if exists). Variable(s): ENVIRONMENT.

```

For more details, see the [docker level `makefile`](./makefile.mk).

Note that some of the default values for `make` variables are defined in the
[repository level `makefile`](../Makefile)

## Useful commands

To (re-)build your core image locally

- using the [`docker-compose.dev.yaml`](./docker-compose.dev.yaml)
- using the ${BASE_IMAGE_TAG} version of its base image,
- using the `development` build stage,
- tagged as `690763002009.dkr.ecr.us-east-1.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}`,

```bash
make docker.build/${IMAGE_NAME}
```

To validate your local core image, run

```bash
make docker.validate/${IMAGE_NAME}
```

For more documentation on a given core image, see the image's dedicated `README.md`.
