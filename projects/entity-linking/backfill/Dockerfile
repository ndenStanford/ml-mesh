ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/beam-backfill:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

ENV USER=app
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

# hadolint ignore=DL3002
USER root

RUN poetry install --no-interaction --no-ansi --only main && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

RUN ln -s /usr/local/bin/python3 /usr/local/bin/python

# switch user
USER ${USER}

# --- production stage
FROM builder as production

ENV PYTHONPATH=${HOME}

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

# hadolint ignore=DL3002
USER root

RUN poetry install --no-interaction --with dev

# switch user
USER ${USER}

# --- debugger stage
FROM builder as debugger

RUN poetry install --no-interaction --with debug
