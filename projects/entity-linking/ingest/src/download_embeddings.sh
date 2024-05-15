#!/usr/bin/env bash
set -e
MODELS_DIR="/home/ec2-user/data/el_embeddings"

mkdir -p "$MODELS_DIR"
cd "$MODELS_DIR"

if [[ ! -f index.txt ]]; then
    wget http://dl.fbaipublicfiles.com/bela/embeddings/index.txt
fi

if [[ ! -f embeddings.pt ]]; then
    wget http://dl.fbaipublicfiles.com/bela/embeddings/embeddings.pt
fi

cd /home/ec2-user/ml-mesh
