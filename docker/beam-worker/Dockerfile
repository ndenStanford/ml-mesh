ARG PYTHON_SHORT_VERSION
ARG BEAM_VERSION

FROM apache/beam_python${PYTHON_SHORT_VERSION}_sdk:${BEAM_VERSION} as builder

ARG IMAGE_NAME
ARG PYTHON_VERSION
ARG PIP_VERSION
ARG POETRY_VERSION

ENV USER=onclusiveml
ENV HOME="/docker/${IMAGE_NAME}"

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

WORKDIR "/"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_VERSION=${PIP_VERSION} \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends \
                            build-essential \
                            ca-certificates \
                            liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# python package management setup
RUN pip3 install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} --no-cache-dir \
    && python3 -V

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users "${POETRY_HOME}"

USER ${USER}

# setup workspace
WORKDIR "/"

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

# install - poetry requirements
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" .${HOME}/

WORKDIR "${HOME}"

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

WORKDIR "${HOME}"

# --- production stage
FROM apache/beam_python${PYTHON_SHORT_VERSION}_sdk:${BEAM_VERSION} as production

COPY --from=builder /usr/local /usr/local

# --- test build stage
FROM production as development
