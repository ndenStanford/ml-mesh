ARG CUDA_VERSION

FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-runtime-ubuntu20.04 as builder

ARG IMAGE_NAME
ARG PYTHON_VERSION=3.8.16
ARG POETRY_VERSION=1.3.2

ENV POETRY_HOME="/home/.poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="${PATH}:/root/.local/bin"

ENV LD_LIBRARY_PATH="/usr/local/cuda-11.6/compat:${LD_LIBRARY_PATH}"

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR "/"

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
        liblzma-dev \
        vim \
        nano \
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
RUN curl -o "Python-${PYTHON_VERSION}.tgz" "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
    && tar -xf "Python-${PYTHON_VERSION}.tgz" \
    && cd "Python-${PYTHON_VERSION}" \
    && ./configure --enable-optimizations --with-ensurepip \
    && make -j $(nproc) \
    && make install \
    && python3 -m pip --no-cache-dir install --upgrade pip setuptools wheel

# create symlink: typing "python" will invoke /usr/local/bin/python3.8
RUN ln -s /usr/local/bin/python3.8 /usr/local/bin/python

# python dependencies
RUN pip3 install poetry==${POETRY_VERSION} --no-cache-dir && \
    python -V

ENTRYPOINT []

# poetry requirements
COPY "docker/${IMAGE_NAME}/poetry.lock" "docker/${IMAGE_NAME}/pyproject.toml" ./

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

FROM builder as development

# install production dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

# develop tests
COPY "docker/${IMAGE_NAME}/tests" "docker/${IMAGE_NAME}/tests"

WORKDIR "/docker/${IMAGE_NAME}"

FROM builder as production
