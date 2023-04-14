ARG OWNER=onclusiveml
ARG IMAGE_NAME=kubeflow-jupyter
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME
FROM $BASE_CONTAINER:$IMAGE_TAG as builder

ENV DOCKER_IMAGE_DIR=docker/kubeflow-torch-cpu

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# switch to NB_UID for installs
USER ${NB_UID}

WORKDIR "${HOME}"

# install - poetry requirements
COPY --chown=${NB_USER}:users ${DOCKER_IMAGE_DIR}/poetry.lock ${DOCKER_IMAGE_DIR}/pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${NB_USER}:users" "${HOME}"

EXPOSE 8888

# --- production stage
FROM builder as production

ENTRYPOINT ["/init"]

# --- test build stage
FROM builder as development

# dummy entrypoint to pass the CI docker run stage
ENTRYPOINT ["pwd"]