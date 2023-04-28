# 'Train' a keybert huggingface model

To run the container step submitting a huggingface model to neptune ai's model registry, run

```docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    onclusiveml/keywords-train:latest \
    python -m src.register_trained_model```