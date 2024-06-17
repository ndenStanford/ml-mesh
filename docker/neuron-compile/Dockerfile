ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$IMAGE_TAG as builder

ARG IMAGE_NAME
ARG PROJECT_DIR="docker/${IMAGE_NAME}"

ENV USER=app

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
    apt-get -yq install --no-install-recommends aws-neuronx-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${PROJECT_DIR}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${PROJECT_DIR}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share \
 && chown -R ${USER}:users /usr/local/include \
 && chown -R ${USER}:users "${POETRY_HOME}"

RUN mkdir -p "${PROJECT_DIR}" && \
    chown -R "${USER}:users" "${PROJECT_DIR}"

# setup workspace
WORKDIR "/"

ENV PATH="/opt/aws/neuron/bin:${PATH}"

# install - production poetry requirements
COPY --chown=${USER}:users "${PROJECT_DIR}/poetry.lock" "${PROJECT_DIR}/pyproject.toml" ./${PROJECT_DIR}/

# copy libraries - ensure relative difference '../..' between PROJECT_DIR app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

WORKDIR "${PROJECT_DIR}"

# install production dependencies
RUN poetry install \
    --only main \
    --no-root \
    --no-interaction \
    --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

RUN pip install \
    tensorflow==1.15.5 \
    --extra-index-url=https://pip.repos.neuron.amazonaws.com/ \
    --no-cache-dir

USER ${USER}

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

# hadolint ignore=DL3002
USER root

# install development dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

WORKDIR "/"

COPY --chown=${USER}:users "${PROJECT_DIR}/tests" "${PROJECT_DIR}/tests"

WORKDIR "${PROJECT_DIR}"
