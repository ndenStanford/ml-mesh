ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/neuron-inference:${BASE_IMAGE_TAG} as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

ENV HOME="${PROJECT_DIR}"

RUN mkdir -p "${HOME}" && \
    chown -R "${USER}:users" "${HOME}"

WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

# required to access mounted docker volume with write permission
# hadolint ignore=DL3002
USER root

# hadolint ignore=DL3008
RUN apt-get update -yq && \
    apt-get install --no-install-recommends gcc \
                    clang \
                    cmake \
                    ninja-build \
                    pkg-config \
                    libgtk-3-dev \
                    liblzma-dev \
                    libstdc++-12-dev \
                    -yq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

USER "${USER}"

# --- production stage
FROM builder as production

# required to access mounted docker volume with write permission
# hadolint ignore=DL3002
USER root

# --- test build stage
FROM production as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

# required to access mounted docker volume with write permission
# hadolint ignore=DL3002
USER root

RUN poetry install --no-interaction --with dev

# --- debugger stage
FROM development as debugger

RUN poetry install --no-interaction --with debug
