ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG
ARG DASK_VERSION
ARG PYTHON_SHORT_VERSION

FROM ghcr.io/dask/dask:${DASK_VERSION}-py${PYTHON_SHORT_VERSION} as builder

ARG IMAGE_NAME
ARG PIP_VERSION
ARG POETRY_VERSION
ARG PYTHON_VERSION

ENV HOME="/docker/${IMAGE_NAME}"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_VERSION=${PIP_VERSION} \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install --no-install-recommends libpq-dev build-essential && \
    apt-get -y install --no-install-recommends curl vim procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# python package management setup
RUN pip install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} --no-cache-dir \
    && python3 -V

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER "${NB_USER}"

# setup workspace
WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown="${NB_UID}:users" ${HOME}/poetry.lock ${HOME}/pyproject.toml ${HOME}/


# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
# hadolint ignore=DL3045
COPY --chown=${NB_UID}:users libs/ libs/

WORKDIR "${HOME}"

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts} && \
    poetry cache clear pypi --all -q

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
 && cp -r "${HOME}" /tmp_home \
 && chown -R "${NB_USER}:users" /tmp_home \
 && chown -R "${NB_USER}:users" ${HOME}

USER "${NB_USER}"

# hadolint ignore=DL3002
USER root

# --- production stage
FROM builder as production


# --- test build stage
FROM builder as development
