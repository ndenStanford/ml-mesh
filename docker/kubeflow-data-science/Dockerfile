ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/kubeflow-torch-cpu:$IMAGE_TAG as builder

ARG IMAGE_NAME

ENV USER=app
ENV HOME="docker/${IMAGE_NAME}"


# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# switch to NB_UID for installs
USER ${NB_UID}

# setup workspace
WORKDIR "/"

# install - poetry requirements
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

WORKDIR "${HOME}"

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${NB_USER}:users" "${HOME}"

EXPOSE 8888

# --- production stage
FROM builder as production

ENTRYPOINT ["/init"]

# --- test build stage
FROM builder as development

# dummy entrypoint to pass the CI docker run stage
ENTRYPOINT ["pwd"]
