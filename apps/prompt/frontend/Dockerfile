FROM node:19-alpine AS builder

ARG APP_NAME
ARG APP_COMPONENT
ARG APP_DIR="apps/${APP_NAME}/${APP_COMPONENT}"

RUN mkdir -p "${HOME}" && \
    chown -R "${USER}:users" "${HOME}"

ENV HOME="${APP_DIR}"

WORKDIR "/"

# Copy the package.json and install dependencies
COPY --chown=${USER}:users ${HOME}/package*.json ./${HOME}/

RUN npm install

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

# Build the project
RUN npx parcel build src/index.html --no-cache --no-source-maps

# --- production stage
FROM builder as production

# --- test build stage
FROM builder as development
