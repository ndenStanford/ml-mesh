ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/kubeflow-jupyter:$IMAGE_TAG as builder

ARG DOCKER_IMAGE_DIR

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# switch to NB_UID for installs
USER ${NB_UID}

WORKDIR "${HOME}"

# install - poetry requirements
COPY --chown=${NB_USER}:users ${DOCKER_IMAGE_DIR}/poetry.lock ${DOCKER_IMAGE_DIR}/pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${NB_USER}:users" "${HOME}"

EXPOSE 8888

# --- production stage
FROM builder as production
ARG DOCKER_IMAGE_DIR

ENTRYPOINT ["/init"]

# --- test build stage
FROM builder as development
ARG DOCKER_IMAGE_DIR

# dummy entrypoint to pass the CI docker run stage
ENTRYPOINT ["pwd"]