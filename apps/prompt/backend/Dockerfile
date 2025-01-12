ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/python-base:$BASE_IMAGE_TAG as builder

ARG APP_NAME
ARG APP_COMPONENT
ARG APP_DIR="/apps/${APP_NAME}/${APP_COMPONENT}"

RUN mkdir -p "${HOME}" && \
    chown -R "${USER}:users" "${HOME}"

ENV HOME="${APP_DIR}"

WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" .${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

USER root

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

RUN eval "$(pyenv init --path)"

USER ${USER}

# --- production stage
FROM builder as production

# --- test build stage
FROM production as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

USER root

RUN poetry install --no-interaction --with dev

USER ${USER}

# --- debugger stage
FROM development as debugger

RUN poetry install --no-interaction --with debug
