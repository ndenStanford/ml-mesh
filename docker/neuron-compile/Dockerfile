ARG OWNER=onclusiveml
ARG IMAGE_NAME=python-base
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME

# --- build stage
FROM $BASE_CONTAINER:$IMAGE_TAG as builder

ENV USER=app
ENV HOME="/home/onclusive/${USER}"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share \
 && chown -R ${USER}:users "${POETRY_HOME}"

USER app

# setup workspace
WORKDIR "${HOME}"

# # install - production poetry requirements
COPY --chown=${USER}:users ./poetry.lock ./pyproject.toml ./

# install production dependencies
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# --- production stage
FROM builder as production

# --- test build stage
FROM production as development

# install test dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"