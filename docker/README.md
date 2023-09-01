# Core docker images

Core docker images are the base images used to power our projects and development environments.

## Images

Images are provided as a way to have a tight dependency management control from development to
production. Often, Deep learning libraries rely on low level components that can be unstable to
manage from one version to another. Moreover, any breaking changes in any of our dependencies
should be caught early on.


| Reference                | Base Image Reference        | Description                                            | Custom Hardware | Validate |
| ------------------------ | ----------------------------| ------------------------------------------------------ | --------------- | -------- |
| `python-base`            | n/a                         | Python base for core and project components            | no              |          |
| `gpu-base`               | `nvidia/cuda` (external)    | Flexible GPU base (w/o torch)                          | gpu             |     x    |
| `gpu-train`              | `python-base`               | GPU base for project train components (w/ torch & hf)  | gpu             |     x    |
| `neuron-compile`         | `python-base`               | Neuron base for project compile components             | inf1            |     x    |
| `neuron-inference`       | `python-base`               | Neuron base for neuron inference-only components       | inf1            |     x    |
| `fastapi-serve`          | `python-base`               | Serving base for project serve components              | no              |          |
| `kubeflow-jupyter`       | `python-base`               | Kubeflow base for jupyter                              | no              |          |
| `kubeflow-torch-cpu`     | `kubeflow-jupyter`          | Kubeflow flavour of flexible pytorch (CPU) image       | no              |          |
| `kubeflow-data-science`  | `kubeflow-torch-cpu`        | DS image for kubeflow                                  | no              |          |

## Dependency management

These images share the same base, and python dependencies are managed in a way that they are tightly
 coupled from one environment to another.

All images that require a `pip-install` have dependencies manged via dependabot and updated every
month.


## Makefile Targets & Docker-Compose Services

We use `make` to consistently call `docker compose` services declared in
- the development [`docker-compose.dev.yaml`](./docker-compose.dev.yaml) and
- the CI [`docker-compose.ci.yaml`](./docker-compose.ci.yaml)

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

## Useful commands

To (re-)build your core image locally

- using the [`docker-compose.dev.yaml`](./docker-compose.dev.yaml)
- using the ${BASE_IMAGE_TAG} version of its base image,
- using the `development` build stage,
- tagged as `063759612765.dkr.ecr.us-east-1.amazonaws.com/${IMAGE_NAME}:${IMAGE_TAG}`,

```bash
make docker.build/${IMAGE_NAME} \
  ENVIRONMENT=dev \
  BASE_IMAGE_TAG=${BASE_IMAGE_TAG} \
  TARGET_BUILD_STAGE=development \
  IMAGE_TAG=${IMAGE_TAG}
```

To validate your local core image, run

```bash
make docker.validate/${IMAGE_NAME} \
  ENVIRONMENT=dev \
  IMAGE_TAG=${IMAGE_TAG}
```

For more documentation on a given core image, see the image's dedicated `README.md`.
