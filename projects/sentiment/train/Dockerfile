ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$BASE_IMAGE_TAG as builder

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
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share

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
FROM builder as production

ENV PYTHONPATH=${HOME}

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

RUN poetry install --no-interaction --with dev

# --- debugger stage
FROM builder as debugger

RUN poetry install --no-interaction --with debug
