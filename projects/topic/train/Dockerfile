ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

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

ARG BERTOPIC_PATH=/pyenv/versions/3.9.19/lib/python3.9/site-packages/bertopic

COPY "${HOME}/modify_bertopic_files.sh" "/usr/local/bin/modify_bertopic_files.sh"

# modify bertopic files
RUN chmod +x /usr/local/bin/modify_bertopic_files.sh && \
    /usr/local/bin/modify_bertopic_files.sh $BERTOPIC_PATH

# --- production stage
FROM builder as production


# --- test build stage
FROM production as development

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

USER ${USER}

# --- debugger stage
FROM development as debugger

RUN poetry install --no-interaction --with debug
