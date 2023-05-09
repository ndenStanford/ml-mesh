# 'Train' a keybert huggingface model

To run the container step submitting a huggingface model to neptune ai's model registry:

1. Set run environment variables:
  - `export OWNER=?`
  - `export IMAGE_TAG=?`
  - `export NEPTUNE_API_TOKEN=?`
2. Run container step:
```docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    -t $OWNER/keywords-train:$IMAGE_TAG \
    python -m src.register_trained_model```