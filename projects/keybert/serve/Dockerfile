ARG OWNER=onclusiveml
ARG IMAGE_NAME=fastapi-serve
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME
FROM $BASE_CONTAINER:$IMAGE_TAG

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

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
COPY --chown=${USER}:users "${PROJECT_DIR}/src" "$HOME/src"

RUN poetry install --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

WORKDIR "${HOME}"