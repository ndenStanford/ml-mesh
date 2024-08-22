ARG UBUNTU_VERSION

FROM ubuntu:${UBUNTU_VERSION} as builder

ARG IMAGE_NAME
ARG PIP_VERSION
ARG POETRY_VERSION
ARG PYTHON_VERSION

ENV HOME="/home"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYENV_ROOT="/pyenv"

ENV PATH="$PYENV_ROOT/shims:${PYENV_ROOT}/bin:$PATH"

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install - usefull linux packages
# hadolint ignore=DL3008
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade \
    && apt-get -yq install --no-install-recommends \
    ca-certificates \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    git \
    && apt-get clean \
    && apt-get remove -yq nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# setup python
RUN curl https://pyenv.run | bash \
    && pyenv install ${PYTHON_VERSION} \
    && eval "$(pyenv init -)"

RUN pyenv global ${PYTHON_VERSION} \
    && pip install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} --no-cache-dir \
    && python -V

# --- production stage
FROM ubuntu:${UBUNTU_VERSION} as production

ARG IMAGE_NAME

ENV HOME="/home"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1 \
    PYENV_ROOT="/pyenv" \
    USER=onclusiveml \
    UID=1002

ENV PATH="$PYENV_ROOT/shims:${PYENV_ROOT}/bin:$PATH"

COPY --from=builder /usr/bin/ /usr/bin/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libsqlite3.so.0 /usr/lib/x86_64-linux-gnu/libsqlite3.so.0
COPY --from=builder /usr/local /usr/local
COPY --from=builder /pyenv /pyenv

# create non root user
RUN useradd -l -M -s /bin/bash -N -u ${UID} ${USER} \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/include \
 && chown -R ${USER}:users "${POETRY_HOME}" \
 && chown -R ${USER}:users "${PYENV_ROOT}"

# --- test build stage
FROM production as development
