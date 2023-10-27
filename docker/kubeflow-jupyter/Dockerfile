ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/python-base:$IMAGE_TAG as builder

ARG IMAGE_NAME

# common environemnt variables
ENV NB_USER=jovyan
ENV NB_UID=1000
ENV NB_PREFIX=/
ENV SHELL=/bin/bash
ENV HOME="/home/${NB_USER}"
#ENV PIP_TARGET="${HOME}/user-pip-packages"
ENV PYTHONPATH="${HOME}/user-pip-packages"

# args - software versions
ARG KUBECTL_ARCH="amd64"
ARG KUBECTL_VERSION=v1.24.0
ARG S6_ARCH="amd64"
# https://skarnet.org/software/s6/
ARG S6_VERSION=v2.2.0.3

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
    ca-certificates \
    curl \
    gcc \
    git \
    gnupg \
    gnupg2 \
    graphviz \
    htop \
    libffi-dev  \
    libssl-dev  \
    locales \
    lsb-release \
    nano \
    npm \
    software-properties-common \
    tzdata \
    unzip \
    vim \
    zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# add the PPA sources for NodeJS 18
RUN curl -s https://deb.nodesource.com/setup_18.x | bash

# hadolint ignore=DL3008
RUN apt-get -yq install --no-install-recommends nodejs

# install - s6 overlay
RUN export GNUPGHOME=/tmp/ \
    && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer" -o /tmp/s6-overlay-${S6_VERSION}-installer \
    && curl -sL "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-${S6_ARCH}-installer.sig" -o /tmp/s6-overlay-${S6_VERSION}-installer.sig \
    && gpg --keyserver keys.gnupg.net --keyserver pgp.surfnet.nl --recv-keys 6101B2783B2FD161 \
    && gpg -q --verify /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer \
    && chmod +x /tmp/s6-overlay-${S6_VERSION}-installer \
    && /tmp/s6-overlay-${S6_VERSION}-installer / \
    && rm /tmp/s6-overlay-${S6_VERSION}-installer.sig /tmp/s6-overlay-${S6_VERSION}-installer

# install - kubectl
RUN curl -sL "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl" -o /usr/local/bin/kubectl \
    && curl -sL "https://dl.k8s.io/${KUBECTL_VERSION}/bin/linux/${KUBECTL_ARCH}/kubectl.sha256" -o /tmp/kubectl.sha256 \
    && echo "$(cat /tmp/kubectl.sha256) /usr/local/bin/kubectl" | sha256sum --check \
    && rm /tmp/kubectl.sha256 \
    && chmod +x /usr/local/bin/kubectl

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

# install - poetry requirements
COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/poetry.lock docker/${IMAGE_NAME}/pyproject.toml ./${HOME}/

COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/.jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py

RUN mkdir "${HOME}/user-pip-packages" \
    && chown "${NB_USER}:users" "${HOME}/user-pip-packages"

RUN touch "${HOME}/test-file" \
    && chown "${NB_USER}:users" "${HOME}/test-file"

# s6 - copy scripts
COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/s6 /etc/

# copy libraries - ensure relative difference '../..' between home app dir and lib as listed in poetry toml
COPY --chown=${USER}:users libs/ libs/

WORKDIR "${HOME}"

COPY --chown="${NB_USER}:users" docker/${IMAGE_NAME}/.config .config

RUN poetry install --no-dev --no-root --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache &&\
    rm -rf ~/.cache/pypoetry/artifacts

RUN poetry cache clear pypi --all -q \
    && chown -R "${NB_USER}:users" "${HOME}"

RUN jupyter lab build --debug

USER root

# s6 - 01-copy-tmp-home
RUN mkdir -p /tmp_home \
    && cp -r "${HOME}" /tmp_home \
    && chown -R "${NB_USER}:users" /tmp_home \
    && chown -R ${NB_USER}:users ${HOME}

USER "${NB_USER}"

EXPOSE 8888

# hadolint ignore=DL3002
USER root

ENTRYPOINT ["/init"]

# --- production stage
FROM builder as production


# --- test build stage
FROM builder as development
