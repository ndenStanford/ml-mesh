FROM node:19-slim AS builder

ARG APP_NAME
ARG APP_COMPONENT
ARG APP_DIR="apps/${APP_NAME}/${APP_COMPONENT}"

ENV USER=app
ENV HOME="/${APP_DIR}"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 101 ${USER} \
 && mkdir -p "${HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib

RUN mkdir -p "${HOME}" && \
    chown -R "${USER}:users" "${HOME}"

WORKDIR "/"

# Copy the package.json and install dependencies
COPY --chown=${USER}:users ${HOME}/package*.json ${HOME}/tsconfig.json ./${HOME}/

# source
COPY --chown=${USER}:users "${HOME}/public" "${HOME}/public"
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

RUN npm install && npm run build

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development

RUN npm install --save-dev
