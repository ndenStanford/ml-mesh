FROM 211212199399.dkr.ecr.us-east-1.amazonaws.com/python-base:v2023.3.2 as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

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

RUN mkdir -p "${HOME}" && \
    mkdir -p "${PROJECT_DIR}" && \
    chown -R "${USER}:users" "${HOME}" && \
    chown -R "${USER}:users" "${PROJECT_DIR}"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${PROJECT_DIR}/poetry.lock" "${PROJECT_DIR}/pyproject.toml" ./

# copy libraries
COPY --chown=${USER}:users libs/ /libs/

# source
COPY --chown=${USER}:users "${PROJECT_DIR}/src" "${HOME}/src"

RUN poetry install --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# --- production stage
WORKDIR "${HOME}"

FROM builder as production

# --- test build stage
FROM builder as development