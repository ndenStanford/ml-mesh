ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:${IMAGE_TAG} as builder

ARG IMAGE_NAME

ENV USER=onclusiveml
ENV HOME="/docker/${IMAGE_NAME}"
ENV POETRY_HOME="${HOME}/.poetry"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1001 ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/include \
 && chown -R ${USER}:users "${POETRY_HOME}"

USER ${USER}

# setup workspace
WORKDIR "/"

# install - poetry requirements
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ${HOME}/

WORKDIR "${HOME}"

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# --- production stage
FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:${IMAGE_TAG} as production

ENV HOME="/home"
ARG IMAGE_NAME

COPY --from=builder /usr/local /usr/local
COPY --from=builder "/docker/${IMAGE_NAME}" ${HOME}

# --- test build stage
FROM production as development
