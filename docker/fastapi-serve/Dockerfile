ARG OWNER=onclusiveml
ARG IMAGE_NAME=python-base
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME
ARG DOCKER_IMAGE_DIR=docker/fastapi-serve

FROM $BASE_CONTAINER:$IMAGE_TAG as builder

ARG DOCKER_IMAGE_DIR

ENV USER=app
ENV HOME="/home"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users "${POETRY_HOME}"

USER app

# setup workspace
WORKDIR "${HOME}"

# install - poetry requirements
COPY --chown=app:users ${DOCKER_IMAGE_DIR}/poetry.lock ${DOCKER_IMAGE_DIR}/pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# --- production stage
FROM builder as production
ARG DOCKER_IMAGE_DIR

# --- test build stage
FROM builder as development
ARG DOCKER_IMAGE_DIR
