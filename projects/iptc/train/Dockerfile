ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="/projects/${PROJECT}/${COMPONENT}"

ENV USER=app
ENV HOME="${PROJECT_DIR}"
ENV POETRY_HOME="${HOME}/.poetry"

# Ensure correct Python version
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.9=3.9.19-1~20.04 \
    python3.9-dev=3.9.19-1~20.04 \
    python3.9-venv=3.9.19-1~20.04 && \
    rm -rf /var/lib/apt/lists/*

# create non root user (currently not provided in gpu base)
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
    && mkdir -p "${HOME}" \
    && mkdir -p "${POETRY_HOME}" \
    && mkdir -p /pyenv \
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

# Set Poetry to use Python 3.9
RUN poetry env use python3.9

RUN poetry install --no-interaction --no-ansi --only main && \
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

RUN poetry install --no-interaction --with dev

# --- debugger stage
FROM development as debugger

RUN poetry install --no-interaction --with debug
