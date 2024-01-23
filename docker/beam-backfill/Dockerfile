FROM apache/flink:1.16-scala_2.12-java11 as builder

ARG IMAGE_NAME
ARG PYTHON_VERSION=3.8.16


ENV USER=app
ENV HOME="docker/${IMAGE_NAME}"

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
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/${HOME}/onclusive/app/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

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

# python
# hadolint ignore=DL3003,SC2046
RUN curl -o Python-${PYTHON_VERSION}.tgz "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
    && tar -xf Python-${PYTHON_VERSION}.tgz \
    && cd  Python-${PYTHON_VERSION} \
    && ./configure --enable-optimizations --with-ensurepip \
    && make -j $(nproc) \
    && make install \
    && python3 -m pip --no-cache-dir install --upgrade pip setuptools wheel

# python package management setup
RUN pip3 install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} apache-flink==1.16 --no-cache-dir \
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

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

USER ${USER}

# setup workspace
WORKDIR "/"

# install - poetry requirements
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

WORKDIR "${HOME}"

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

# python SDK
COPY --from=apache/beam_python3.8_sdk:2.49.0 /opt/apache/beam /opt/apache/beam

WORKDIR "${HOME}"

# --- production stage
FROM builder as production


# --- test build stage
FROM builder as development
