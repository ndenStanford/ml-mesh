ARG CUDA_VERSION
ARG UBUNTU_VERSION

FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-runtime-ubuntu${UBUNTU_VERSION} as builder

ARG IMAGE_NAME
ARG PYTHON_VERSION
ARG POETRY_VERSION
ARG PIP_VERSION

ENV HOME="/docker/${IMAGE_NAME}"

ENV POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYENV_ROOT="/pyenv"

ENV PATH="$PYENV_ROOT/shims:${PYENV_ROOT}/bin:$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

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

# poetry requirements
COPY "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./

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

FROM nvidia/cuda:${CUDA_VERSION}-cudnn8-runtime-ubuntu${UBUNTU_VERSION} as production

ENV HOME="/home"

COPY --from=builder /usr/local /usr/local
COPY --from=builder /pyenv /pyenv

FROM production as development
