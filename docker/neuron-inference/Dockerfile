ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:${BASE_IMAGE_TAG} as builder

ARG IMAGE_NAME

ENV USER=onclusiveml
ENV HOME="/docker/${IMAGE_NAME}"

USER root

# get wget and gnupg2 tools
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -yq install --no-install-recommends wget gnupg2 ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Linux for Neuron repository updates
RUN echo 'deb https://apt.repos.neuron.amazonaws.com bionic main' >> /etc/apt/sources.list.d/neuron.list
# hadolint ignore=DL4006
RUN wget -qO - https://apt.repos.neuron.amazonaws.com/GPG-PUB-KEY-AMAZON-AWS-NEURON.PUB | apt-key add -

# Install Neuron Driver
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get -yq install --no-install-recommends aws-neuronx-tools aws-neuronx-dkms && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1001 ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local \
 && chown -R ${USER}:users "${POETRY_HOME}"

# switch user
USER ${USER}

# setup workspace

WORKDIR "/"

ENV PATH="/opt/aws/neuron/bin:$PATH"

# install - production poetry requirements
COPY --chown=${USER}:users ${HOME}/poetry.lock ${HOME}/pyproject.toml .${HOME}/

WORKDIR "${HOME}"

# install production dependencies
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# --- production stage
FROM builder as production

ENV HOME="/home"

WORKDIR "${HOME}"

# --- test build stage
FROM production as development
