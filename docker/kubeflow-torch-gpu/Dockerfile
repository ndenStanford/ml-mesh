ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:${BASE_IMAGE_TAG} as builder

ARG IMAGE_NAME
ARG S6_VERSION
ARG AWS_CLI_VERSION
ARG KUBECTL_VERSION
ARG NODE_VERSION
ARG PYTHON_VERSION

# common environemnt variables
ENV NB_USER=jovyan \
    NB_UID=1001 \
    NB_PREFIX=/ \
    SHELL=/bin/bash \
    POETRY_VIRTUALENVS_CREATE=false \
    NB_GID=0 \
    USERS_GID=100

# s6-overlay only gives 5 seconds by default, which is too small for slow PVC storage backends
# when running `/etc/cont-inid.d/01-copy-tmp-home` (note, this is in milliseconds)
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME 300000

# s6-overlay does not fail by default if the `/etc/cont-init.d/` or `/etc/services.d/` scripts fail
# this is not the desired behavior, so we set it to fail
ENV S6_BEHAVIOUR_IF_STAGE2_FAILS 2

ENV HOME="/home/${NB_USER}" \
    HOME_TMP=/tmp_home/${NB_USER}
ENV POETRY_HOME="${HOME}"
ENV NVM_DIR="${HOME}/.nvm"
ENV PATH="$NVM_DIR:$PATH"

# args - software versions
ARG KUBECTL_ARCH="amd64"
ARG S6_ARCH="x86_64"
ARG KUBECTL_VERSION=${KUBECTL_VERSION}
ARG AWS_CLI_VERSION=${AWS_CLI_VERSION}

# set shell to bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install - usefull linux packages
# hadolint ignore=DL3008
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -yq update \
    && apt-get -yq upgrade \
    && apt-get -yq install --no-install-recommends \
    apt-transport-https \
    bash \
    bzip2 \
    wget \
    curl \
    gcc \
    git \
    gnupg \
    gnupg2 \
    graphviz \
    htop \
    libffi-dev  \
    libssl-dev  \
    sqlite3 \
    libsqlite3-dev \
    locales \
    lsb-release \
    nano \
    software-properties-common \
    tzdata \
    unzip \
    vim \
    procps \
    zip \
    xz-utils \
    && apt-get clean \
    && apt-get remove -yq nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# installs nvm (Node Version Manager)
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

# hadolint ignore=SC1091
RUN . ${HOME}/.nvm/nvm.sh && nvm install ${NODE_VERSION} && nvm use ${NODE_VERSION}

# install - s6 overlay
# hadolint ignore=SC2002
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

RUN chmod 0775 /run

# install - kubectl
RUN curl -sL "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl" -o /usr/local/bin/kubectl \
    && curl -sL "https://dl.k8s.io/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl.sha256" -o /tmp/kubectl.sha256 \
    && echo "$(cat /tmp/kubectl.sha256) /usr/local/bin/kubectl" | sha256sum --check \
    && rm /tmp/kubectl.sha256 \
    && chmod +x /usr/local/bin/kubectl

# install aws cli
# hadolint ignore=DL4001
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64-${AWS_CLI_VERSION}.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

WORKDIR "/"

# create user and set required ownership
# new user is not added to lastlog and faillog databases
# https://stackoverflow.com/questions/48671214/docker-image-size-for-different-user
RUN useradd -M -N --shell /bin/bash --home ${HOME} --uid ${NB_UID} --groups ${USERS_GID} --gid ${NB_GID} ${NB_USER} \
    && mkdir -pv ${HOME} \
    && mkdir -pv ${HOME}/.local \
    && mkdir -pv ${HOME_TMP} \
    && chmod 2775 ${HOME} \
    && chmod 2775 ${HOME_TMP} \
    && chown -R ${NB_USER}:users ${HOME} \
    && chown -R ${NB_USER}:users /usr/local \
    && chown -R ${NB_USER}:users /etc/profile \
    && chown -R ${NB_USER}:users ${HOME_TMP} \
    && chown -R ${NB_USER}:users /usr/local/bin \
    && chown -R ${NB_USER}:users ${HOME}/.local \
    && chown -R ${NB_USER}:users "${PYENV_ROOT}"

# set locale configs
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
 && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# switch to NB_UID for installs
USER "${NB_UID}"

# install - poetry requirements
COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/poetry.lock docker/${IMAGE_NAME}/pyproject.toml .${HOME}/

# create the SYSTEM_CONFIG_PATH for jupyter, and make it owned by NB_USER
# this is needed for jupyter to write `--level=system` configs
RUN mkdir -pv /usr/local/etc/jupyter \
 && chown -R ${NB_USER}:${NB_GID} /usr/local/etc/jupyter

 # switch to NB_UID for installs
USER $NB_UID

# s6 - copy scripts
COPY --chown=${NB_USER}:${NB_GID} --chmod=755 docker/${IMAGE_NAME}/s6 /etc/

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

WORKDIR "${HOME}"


RUN poetry install --only main --no-root --no-interaction --no-ansi && \
   rm -rf ~/.cache/pypoetry/{cache,artifacts}

RUN poetry cache clear pypi --all -q \
   && chown -R "${NB_USER}:users" "${HOME}"

# hadolint ignore=SC1091
RUN . ${HOME}/.nvm/nvm.sh && nvm use ${NODE_VERSION} && python -m jupyter lab build --debug

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
    && cp -r "${HOME}" /tmp_home \
    && chown -R "${NB_USER}:users" /tmp_home

EXPOSE 8888


ENTRYPOINT ["/init"]

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development
