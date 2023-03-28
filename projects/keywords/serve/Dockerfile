FROM 211212199399.dkr.ecr.us-east-1.amazonaws.com/fastapi-serve:v2023.3.2 as builder

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

RUN poetry install --no-interaction

WORKDIR "${HOME}"
