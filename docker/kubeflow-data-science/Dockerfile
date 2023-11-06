ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/kubeflow-torch-cpu:$IMAGE_TAG as builder

ARG IMAGE_NAME

ENV HOME="/home/${NB_USER}"


# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# switch to NB_UID for installs
USER ${NB_UID}

# setup workspace
WORKDIR "/"

# install - poetry requirements
COPY --chown=${NB_USER}:users docker/${IMAGE_NAME}/poetry.lock docker/${IMAGE_NAME}/pyproject.toml ./${HOME}/

WORKDIR "${HOME}"

# install python dependencies into configured virtual environment at /home/jovyan
RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${NB_USER}:users" "${HOME}"

EXPOSE 8888

# hadolint ignore=DL3002
USER root

ENTRYPOINT ["/init"]

# --- production stage
FROM builder as production


# --- test build stage
FROM builder as development
