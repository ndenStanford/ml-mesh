ARG FLINK_VERSION
ARG SCALA_VERSION
ARG JAVA_VERSION
ARG BEAM_VERSION

FROM apache/flink:${FLINK_VERSION}-scala_${SCALA_VERSION}-java${JAVA_VERSION} as builder

ARG IMAGE_NAME
ARG PYTHON_VERSION
ARG BEAM_VERSION
ARG PYTHON_SHORT_VERSION
ARG JAVA_VERSION
ARG FLINK_VERSION

ENV HOME="/docker/${IMAGE_NAME}"

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

WORKDIR "/"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_VERSION=22.3.1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.0 \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1 \
    PYENV_ROOT="/pyenv"

ENV PATH="$PYENV_ROOT/shims:${PYENV_ROOT}/bin:$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# hadolint ignore=DL3008
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qy \
    && apt-get install \
        -y \
        --reinstall build-essential \
        --no-install-recommends \
        curl \
        make \
        gcc \
        git \
        openssh-server \
        build-essential \
        zlib1g-dev \
        libncurses5-dev \
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libreadline-dev \
        libffi-dev \
        libsqlite3-dev \
        libbz2-dev \
        libpq-dev \
        lzma \
        liblzma-dev \
        unzip \
        ca-certificates \
        groff \
        mandoc \
        sudo \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# setup python
RUN curl https://pyenv.run | bash \
    && pyenv install ${PYTHON_VERSION} \
    && eval "$(pyenv init -)"

RUN pyenv global ${PYTHON_VERSION} \
    && pip install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} --no-cache-dir \
    && python -V

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# setup workspace
WORKDIR "/"

# install - poetry requirements
COPY "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

WORKDIR "${HOME}"

USER ${USER}

# --- production stage
FROM apache/flink:${FLINK_VERSION}-scala_${SCALA_VERSION}-java${JAVA_VERSION} as production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1 \
    PYENV_ROOT="/pyenv" \
    USER=onclusiveml \
    UID=1002

# python SDK
COPY --from=apache/beam_python3.9_sdk:2.58.0 /opt/apache/beam /opt/apache/beam
COPY --from=builder /usr/local /usr/local
COPY --from=builder "/docker/${IMAGE_NAME}" ${HOME}
COPY --from=builder /pyenv /pyenv

# create non root user
RUN useradd -l -M -s /bin/bash -N -u ${UID} ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users "${PYENV_ROOT}" \
 && chown -R ${USER}:users /usr/local \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users "${POETRY_HOME}"

# --- test build stage
FROM production as development
