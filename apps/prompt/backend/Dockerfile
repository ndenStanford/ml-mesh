FROM 063759612765.dkr.ecr.us-east-1.amazonaws.com/fastapi-serve:v2023.3.1 as builder

ARG APP_NAME
ARG APP_COMPONENT
ARG APP_DIR="apps/${APP_NAME}/${APP_COMPONENT}"

RUN mkdir -p "${HOME}" && \
    chown -R "${USER}:users" "${HOME}"

ENV HOME="${APP_DIR}"

WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

RUN poetry install --without dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

RUN poetry install --no-interaction
