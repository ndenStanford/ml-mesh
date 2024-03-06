ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

ENV USER=app

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
    && mkdir -p "${PROJECT_DIR}" \
    && mkdir -p "${POETRY_HOME}" \
    && chown -R ${USER}:users "${HOME}" \
    && chown -R ${USER}:users "${PROJECT_DIR}" \
    && chown -R ${USER}:users "${POETRY_HOME}" \
    && chown -R ${USER}:users /usr/local/bin \
    && chown -R ${USER}:users /usr/local/lib \
    && chown -R ${USER}:users /usr/local/share

USER root

# setup workspace
WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${PROJECT_DIR}/poetry.lock" "${PROJECT_DIR}/pyproject.toml" ./${PROJECT_DIR}/

# copy libraries
COPY --chown=${USER}:users libs/core libs/core
COPY --chown=${USER}:users libs/tracking libs/tracking

# source
COPY --chown=${USER}:users "${PROJECT_DIR}/src" "${PROJECT_DIR}/src"

WORKDIR "${PROJECT_DIR}"

RUN poetry install --no-interaction --no-ansi --only main && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

USER app

# --- production stage
FROM builder as production

USER app

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${PROJECT_DIR}/tests" "${PROJECT_DIR}/tests"

WORKDIR "${PROJECT_DIR}"

RUN poetry install \
    --with dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

USER app

# --- debugger stage
FROM builder as debugger

RUN poetry install --no-interaction --with debug
