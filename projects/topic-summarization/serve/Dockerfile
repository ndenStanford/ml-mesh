ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/fastapi-serve:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

# hadolint ignore=DL3002
USER root

RUN mkdir -p "${PROJECT_DIR}" && \
    chown -R "${USER}:users" "${PROJECT_DIR}" && \
    chown -R "${USER}:users" "/usr/local/share"

WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${PROJECT_DIR}/poetry.lock" "${PROJECT_DIR}/pyproject.toml" ./${PROJECT_DIR}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${PROJECT_DIR}/src" "${PROJECT_DIR}/src"

WORKDIR "${PROJECT_DIR}"

RUN poetry install --without dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    MINIMAL_KATS=1 pip install --no-cache-dir kats==0.2.0

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

WORKDIR "/"

COPY --chown=${USER}:users "${PROJECT_DIR}/tests" "${PROJECT_DIR}/tests"

WORKDIR "${PROJECT_DIR}"

RUN poetry install --no-interaction

USER ${USER}
