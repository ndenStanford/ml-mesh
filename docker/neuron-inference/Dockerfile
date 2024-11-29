ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/python-base:${BASE_IMAGE_TAG} as builder

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

# switch user
USER ${USER}

# setup workspace

WORKDIR "/"

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
FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/python-base:${BASE_IMAGE_TAG} as production

ENV HOME="/home"
ENV PATH="/opt/aws/neuron/bin:$PATH"

COPY --from=builder /usr/local /usr/local
COPY --from=builder /pyenv /pyenv

WORKDIR "${HOME}"

# --- test build stage
FROM production as development
