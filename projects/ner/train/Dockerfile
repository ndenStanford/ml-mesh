ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/python-base:$BASE_IMAGE_TAG AS builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

ENV USER=app
ENV HOME="${PROJECT_DIR}"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users "${POETRY_HOME}" \
 && chown -R ${USER}:users /usr/local/ \
 && chown -R ${USER}:users /pyenv/

USER app

# setup workspace
WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

RUN poetry install --no-interaction --no-ansi --only main && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# --- production stage
FROM builder AS production

ENV PYTHONPATH=${HOME}

# --- test build stage
FROM builder AS development

# install development dependencies
RUN poetry install \
    --with dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

COPY --chown=${USER}:users "${HOME}/tests" ./tests

# --- debugger stage
FROM builder AS debugger

RUN poetry install --no-interaction --with debug
