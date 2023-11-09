ARG AWS_ACCOUNT_ID
ARG BASE_IMAGE_TAG

FROM ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/gpu-base:$BASE_IMAGE_TAG as builder

ARG PROJECT
ARG COMPONENT
ARG PROJECT_DIR="projects/${PROJECT}/${COMPONENT}"

ENV USER=app
ENV HOME="${PROJECT_DIR}"

# create non root user
RUN useradd -l -M -s /bin/bash -N -u 1000 app \
 && mkdir -p "${HOME}" \
 && mkdir -p "${POETRY_HOME}" \
 && chown -R ${USER}:users "${HOME}" \
 && chown -R ${USER}:users "${POETRY_HOME}" \
 && chown -R ${USER}:users /usr/local/bin \
 && chown -R ${USER}:users /usr/local/lib \
 && chown -R ${USER}:users /usr/local/share

# setup workspace
WORKDIR "/"

# install - poetry requirements
# hadolint ignore=DL3045
COPY --chown=${USER}:users "${HOME}/poetry.lock" "${HOME}/pyproject.toml" ./${HOME}/

# copy libraries
COPY --chown=${USER}:users libs/ libs/

# source
COPY --chown=${USER}:users "${HOME}/src" "${HOME}/src"

WORKDIR "${HOME}"

# hadolint ignore=DL3002
USER root

RUN poetry install --no-interaction --no-ansi && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q

RUN sed -i '/from umap import UMAP/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/_bertopic.py && \
    sed -i 's/: UMAP//g' /usr/local/lib/python3.8/site-packages/bertopic/_bertopic.py && \
    sed -i ':a;N;$!ba;s/or[[:space:]]\+UMAP([^)]\+self\.low_memory)//' /usr/local/lib/python3.8/site-packages/bertopic/_bertopic.py && \
    sed -i '/from umap import UMAP/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_topics.py && \
    sed -i '/embeddings = UMAP(n_neighbors=2, n_components=2, metric='"'"'hellinger'"'"', random_state=42).fit_transform(embeddings)/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_topics.py && \
    sed -i '/embeddings = UMAP(n_neighbors=2, n_components=2, metric='"'"'cosine'"'"', random_state=42).fit_transform(embeddings)/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_topics.py && \
    sed -i '/from umap import UMAP/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_hierarchical_documents.py && \
    sed -i '/umap_model = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='"'"'cosine'"'"').fit(embeddings_to_reduce)/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_hierarchical_documents.py && \
    sed -i 's/embeddings_2d = umap_model.embedding_/pass/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_hierarchical_documents.py && \
    sed -i '/from umap import UMAP/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_documents.py && \
    sed -i '/umap_model = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='"'"'cosine'"'"').fit(embeddings_to_reduce)/s/^/#/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_documents.py && \
    sed -i 's/embeddings_2d = umap_model.embedding_/pass/' /usr/local/lib/python3.8/site-packages/bertopic/plotting/_documents.py


# --- production stage
FROM builder as production

USER app

# --- test build stage
FROM builder as development

# install development dependencies
RUN poetry install \
    --only dev \
    --no-root \
    --no-interaction \
    --no-ansi \
    -v && \
    rm -rf ~/.cache/pypoetry/cache && \
    rm -rf ~/.cache/pypoetry/artifacts && \
    poetry cache clear pypi --all -q && \
    chown -R "${USER}:users" "${HOME}"

COPY --chown=${USER}:users "${HOME}/tests" ./tests

USER app
