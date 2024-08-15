FROM ubuntu:22.04 as builder

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
    apt-get -y install --no-install-recommends \
                            libpq-dev \
                            zlib1g-dev \
                            build-essential \
                            ca-certificates \
                            sqlite-devel \
                            curl \
                            vim \
                            procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# python
# hadolint ignore=DL3003,SC2046
RUN curl -o "Python-${PYTHON_VERSION}.tgz" "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
    && tar -xf "Python-${PYTHON_VERSION}.tgz" \
    && cd "Python-${PYTHON_VERSION}" \
    && ./configure --enable-optimizations --with-ensurepip \
    && make -j $(nproc) \
    && make install \
    && python3 -m pip --no-cache-dir install --upgrade pip setuptools wheel

# python package management setup
RUN pip install --upgrade pip==${PIP_VERSION} poetry==${POETRY_VERSION} --no-cache-dir \
    && python3 -V

# --- production stage
FROM ubuntu:22.04 as production

ARG IMAGE_NAME

ENV HOME="/home"
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="${HOME}/.poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1

COPY --from=builder /usr/local /usr/local

# --- test build stage
FROM production as development
