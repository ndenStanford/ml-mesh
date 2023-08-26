ARG AWS_ACCOUNT_ID
ARG IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:$IMAGE_TAG as builder

ARG IMAGE_NAME

ENV HOME="docker/${IMAGE_NAME}"

# common environemnt variables
ENV NB_USER=jovyan
ENV NB_UID=1000
ENV NB_PREFIX=/
ENV SHELL=/bin/bash

# install - usefull linux packages
# hadolint ignore=DL3008
RUN export DEBIAN_FRONTEND=noninteractive \
 && apt-get -yq update \
 && apt-get -yq install --no-install-recommends \
    apt-transport-https \
    bash \
    bzip2 \
    ca-certificates \
    gnupg \
    gnupg2 \
    htop \
    locales \
    lsb-release \
    nano \
    npm \
    software-properties-common \
    tzdata \
    vim \
    zip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*


USER "${NB_USER}"

EXPOSE 8888

# hadolint ignore=DL3002
USER root

ENTRYPOINT ["/init"]
