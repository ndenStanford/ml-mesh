ARG PYTHON_VERSION=3.8.16

FROM python:${PYTHON_VERSION}-slim as builder

ARG IMAGE_NAME

ENV USER=app
ENV HOME="docker/${IMAGE_NAME}"

ENV HOME="/home"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_VERSION=22.3.1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/${HOME}/onclusive/app/.poetry" \
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
    && python -V

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development
