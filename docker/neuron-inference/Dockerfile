ARG OWNER=onclusiveml
ARG IMAGE_NAME=python-base
ARG IMAGE_TAG=latest
ARG BASE_CONTAINER=$OWNER/$IMAGE_NAME

# --- build stage
FROM $BASE_CONTAINER:$IMAGE_TAG as builder

ARG DOCKER_IMAGE_DIR=docker/neuron-inference

USER root

# get wget and gnupg2 tools
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -yq install --no-install-recommends wget gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Linux for Neuron repository updates
RUN echo 'deb https://apt.repos.neuron.amazonaws.com bionic main' >> /etc/apt/sources.list.d/neuron.list
# hadolint ignore=DL4006
RUN wget -qO - https://apt.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB | apt-key add -

# Install Neuron Driver
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -yq install --no-install-recommends aws-neuronx-dkms aws-neuronx-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV USER=app
ENV HOME="/home/onclusive/${USER}"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share \
 && chown -R ${USER}:users "${POETRY_HOME}"

USER app

# setup workspace
WORKDIR "${HOME}"

RUN export PATH=/opt/aws/neuron/bin:$PATH

# install - production poetry requirements
COPY --chown=${USER}:users ${DOCKER_IMAGE_DIR}/poetry.lock ${DOCKER_IMAGE_DIR}/pyproject.toml ./

# install production dependencies
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi && \
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
    --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

COPY --chown=${USER}:users ${DOCKER_IMAGE_DIR}/tests/ ./tests

RUN mkdir tests/output
