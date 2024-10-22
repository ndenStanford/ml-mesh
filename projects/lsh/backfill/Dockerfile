ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/beam-backfill:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="/projects/${PROJECT}/${COMPONENT}"

ENV HOME="${PROJECT_DIR}"

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

# switch user
USER ${USER}

RUN poetry install --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# --- production stage
FROM builder as production

ENV PYTHONPATH=${HOME}

# --- test build stage
FROM production as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

RUN poetry install --no-interaction
