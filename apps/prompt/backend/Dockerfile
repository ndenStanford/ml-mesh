ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/fastapi-serve:$BASE_IMAGE_TAG as builder

ARG APP_NAME
ARG APP_COMPONENT
ARG APP_DIR="/apps/${APP_NAME}/${APP_COMPONENT}"

RUN mkdir -p "${APP_DIR}" && \
    chown -R "${USER}:users" "${APP_DIR}"

WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${APP_DIR}/poetry.lock" "${APP_DIR}/pyproject.toml" ./${APP_DIR}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${APP_DIR}/src" "${APP_DIR}/src"

WORKDIR "${APP_DIR}"

USER root

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${APP_DIR}"

USER ${USER}

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${APP_DIR}/tests" "${APP_DIR}/tests"

WORKDIR "${APP_DIR}"

USER root

RUN poetry install --no-interaction --with dev

USER ${USER}

# --- debugger stage
FROM builder as debugger

RUN poetry install --no-interaction --with debug
