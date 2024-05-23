ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="/projects/${PROJECT}/${COMPONENT}"

ENV HOME="${PROJECT_DIR}"

# hadolint ignore=DL3002
USER root

# setup workspace
WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/core/ libs/core/
COPY --chown=${USER}:users libs/tracking/ libs/tracking/

WORKDIR "${HOME}"

RUN poetry install --no-interaction --no-ansi --only main && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

WORKDIR "${HOME}"

RUN poetry install --no-interaction --with dev

# --- debugger stage
FROM builder as debugger

RUN poetry install --no-interaction --with debug
