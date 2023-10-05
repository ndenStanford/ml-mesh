ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ghcr.io/dask/dask:2023.3.1-py3.8 as builder

ARG IMAGE_NAME

ENV HOME="/home"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_VERSION=22.3.1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# hadolint ignore=DL4006
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.3.2 python3 -

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
    && python -V
# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# switch to NB_UID for installs
USER "${NB_UID}"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown="${NB_UID}:users" docker/${IMAGE_NAME}/poetry.lock docker/${IMAGE_NAME}/pyproject.toml ./${HOME}/

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
# hadolint ignore=DL3045
COPY --chown=${NB_UID}:users libs/ libs/

WORKDIR "${HOME}"

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts}

RUN poetry cache clear pypi --all -q

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
