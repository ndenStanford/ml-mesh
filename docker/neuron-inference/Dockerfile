ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$IMAGE_TAG as builder

ARG IMAGE_NAME

ENV USER=app
ENV HOME="docker/${IMAGE_NAME}"

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
RUN useradd -l -M -s /bin/bash -N -u 1000 ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share \
 && chown -R ${USER}:users /usr/local/include \
 && chown -R ${USER}:users "${POETRY_HOME}"

# switch user
USER ${USER}

# setup workspace

WORKDIR "/"

ENV PATH="/opt/aws/neuron/bin:$PATH"

# install - production poetry requirements
COPY --chown=${USER}:users ${HOME}/poetry.lock ${HOME}/pyproject.toml ./${HOME}/

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


# --- test build stage - generate neuron compiled model artifacts as inputs for testing in dev stage
FROM builder as builder-compilation

ARG NEURON_COMPILE_OUTPUT_DIR

# install compilation dependencies
RUN poetry install \
    --only compilation \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

RUN pip install \
    tensorflow==1.15.5 \
    --extra-index-url=https://pip.repos.neuron.amazonaws.com/ \
    --no-cache-dir

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

RUN pytest tests/core -ra -vv --capture=no -m compilation

# --- test build stage
FROM builder as development

ARG NEURON_COMPILE_OUTPUT_DIR

# install development dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

WORKDIR "/"

COPY --chown=${USER}:users "${HOME}/tests" "${HOME}/tests"

WORKDIR "${HOME}"

COPY --from=builder-compilation --chown=$(USER):users "/${HOME}/${NEURON_COMPILE_OUTPUT_DIR}" "${NEURON_COMPILE_OUTPUT_DIR}"

# hadolint ignore=DL3002
USER root

RUN echo "${NEURON_COMPILE_OUTPUT_DIR}" \
    && chown -R "${USER}:users" "${NEURON_COMPILE_OUTPUT_DIR}" \
    && ls -l "${NEURON_COMPILE_OUTPUT_DIR}"
