ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:${BASE_IMAGE_TAG} as builder

ARG IMAGE_NAME
ARG S6_VERSION
ARG AWS_CLI_VERSION
ARG KUBECTL_VERSION
ARG NODE_VERSION
ARG POETRY_VERSION

# common environemnt variables
ENV NB_USER=jovyan
ENV NB_UID=1001
ENV NB_PREFIX=/
ENV SHELL=/bin/bash
ENV HOME="/home/${NB_USER}"
ENV POETRY_HOME="${HOME}"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV NVM_DIR=${HOME}/.nvm
ENV PATH="$NVM_DIR:$PATH"

# args - software versions
ARG KUBECTL_ARCH="amd64"
ARG KUBECTL_VERSION=${KUBECTL_VERSION}
ARG S6_ARCH="amd64"
# https://skarnet.org/software/s6/
ARG S6_VERSION=${S6_VERSION}
ARG AWS_CLI_VERSION=${AWS_CLI_VERSION}

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# install - usefull linux packages
# hadolint ignore=DL3008
RUN export DEBIAN_FRONTEND=noninteractive \
   && apt-get -yq update \
   && apt-get -yq install --no-install-recommends \
   apt-transport-https \
   bash \
   bzip2 \
   gnupg \
   gnupg2 \
   htop \
   locales \
   lsb-release \
   nano \
   sqlite3 \
   libsqlite3-dev \
   npm \
   software-properties-common \
   tzdata \
   vim \
   zip \
   && apt-get clean \
   && apt-get remove -yq nodejs npm \
   && rm -rf /var/lib/apt/lists/*

# installs nvm (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

RUN . ${HOME}/.nvm/nvm.sh && nvm install ${NODE_VERSION} && nvm use ${NODE_VERSION}

# install - s6 overlay
RUN curl -fsSL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-noarch.tar.xz" -o /tmp/s6-overlay-noarch.tar.xz \
 && curl -fsSL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-noarch.tar.xz.sha256" -o /tmp/s6-overlay-noarch.tar.xz.sha256 \
 && echo "$(cat /tmp/s6-overlay-noarch.tar.xz.sha256 | awk '{ print $1; }')  /tmp/s6-overlay-noarch.tar.xz" | sha256sum -c - \
 && curl -fsSL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz" -o /tmp/s6-overlay-${S6_ARCH}.tar.xz \
 && curl -fsSL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}.tar.xz.sha256" -o /tmp/s6-overlay-${S6_ARCH}.tar.xz.sha256 \
 && echo "$(cat /tmp/s6-overlay-${S6_ARCH}.tar.xz.sha256 | awk '{ print $1; }')  /tmp/s6-overlay-${S6_ARCH}.tar.xz" | sha256sum -c - \
 && tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz \
 && tar -C / -Jxpf /tmp/s6-overlay-${S6_ARCH}.tar.xz \
 && rm /tmp/s6-overlay-noarch.tar.xz  \
       /tmp/s6-overlay-noarch.tar.xz.sha256 \
       /tmp/s6-overlay-${S6_ARCH}.tar.xz \
       /tmp/s6-overlay-${S6_ARCH}.tar.xz.sha256

# install - kubectl
RUN curl -sL "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl" -o /usr/local/bin/kubectl \
   && curl -sL "https://dl.k8s.io/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl.sha256" -o /tmp/kubectl.sha256 \
   && echo "$(cat /tmp/kubectl.sha256) /usr/local/bin/kubectl" | sha256sum --check \
   && rm /tmp/kubectl.sha256 \
   && chmod +x /usr/local/bin/kubectl

# install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

WORKDIR "/"

# create user and set required ownership
# new user is not added to lastlog and faillog databases
# https://stackoverflow.com/questions/48671214/docker-image-size-for-different-user
RUN useradd -l -M -s /bin/bash -N -u ${NB_UID} ${NB_USER} \
   && mkdir -p ${HOME} \
   && chown -R ${NB_USER}:users ${HOME} \
   && chown -R ${NB_USER}:users /usr/local \
   && chown -R ${NB_USER}:users /etc/profile

### set locale configs
RUN echo "en_GB.UTF-8 UTF-8" > /etc/locale.gen \
   && locale-gen
ENV LANG en_GB.UTF-8
ENV LANGUAGE en_GB.UTF-8
ENV LC_ALL en_GB.UTF-8

# switch to NB_UID for installs
USER "${NB_UID}"

# install and activate venv to ensure poetry installed python packages end up on mounted volume
# source: https://github.com/python-poetry/poetry/issues/1579#issuecomment-863737675
ENV VIRTUAL_ENV="${HOME}/venv"
RUN python -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# install - poetry requirements
COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/poetry.lock docker/${IMAGE_NAME}/pyproject.toml .${HOME}/

COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/.jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

# s6 - copy scripts
COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/s6 /etc/

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

WORKDIR "${HOME}"

RUN poetry install --only main --no-root --no-interaction --no-ansi && \
   rm -rf ~/.cache/pypoetry/{cache,artifacts}

RUN poetry cache clear pypi --all -q \
   && chown -R "${NB_USER}:users" "${HOME}"

RUN . ${HOME}/.nvm/nvm.sh && nvm use ${NODE_VERSION} && python -m jupyter lab build --debug

USER root

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
    && cp -r "${HOME}" /tmp_home \
    && chown -R "${NB_USER}:users" /tmp_home

USER "${NB_USER}"

EXPOSE 8888

# hadolint ignore=DL3002
USER root

ENTRYPOINT ["/init"]

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development
