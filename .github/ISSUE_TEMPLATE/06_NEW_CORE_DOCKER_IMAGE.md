---
name: New Core Docker Image
description: New core docker image checklist.
title: "[DOCKER]: "
labels: ["docker"]
about: Adding a new core docker image to the codebase.
assignees: ""
---

### **Checklist**

- [ ] create a new folder `docker/<image name>/` with your image name.
- [ ] add the `Dockerfile` and the image content.

```dockerfile
ARG OWNER=onclusiveml
ARG IMAGE_NAME=python-base
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME
FROM $BASE_CONTAINER:$IMAGE_TAG

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# switch to NB_UID for installs
USER ${NB_UID}

WORKDIR "${HOME}"

```

- [ ] initialise the project by running the command `poetry init` if you need to install python libraries. Add this block to your dockerfile

```dockerfile
# install - poetry requirements
COPY --chown=app:users ./poetry.lock ./pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${NB_USER}:users" "${HOME}"

```

- [ ] open an issue in [ml-platform](https://github.com/AirPR/ml-platform/blob/prod/.github/ISSUE_TEMPLATE/04_NEW_ECR_REPOSITORY.md) to create a new ECR repository with the name `<image name>`.
- [ ] get a PR started from your feature branch to `stage`.

---
