ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$IMAGE_TAG as builder

ARG IMAGE_NAME

ENV USER=app
ENV HOME="docker/${IMAGE_NAME}"

USER root

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local \
 && chown -R ${USER}:users "${POETRY_HOME}"

# switch user
USER ${USER}

# setup workspace

WORKDIR "/"

# install - production poetry requirements
COPY --chown=${USER}:users ${HOME}/poetry.lock ${HOME}/pyproject.toml ./${HOME}/

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

WORKDIR "${HOME}"

# install production dependencies
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# --- production stage
FROM builder as production


# --- test build stage
FROM builder as development

# install development dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

COPY --chown=${USER}:users "${HOME}/tests" ./tests
