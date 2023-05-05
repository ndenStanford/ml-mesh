# 'Train' a keybert huggingface model

To run the container step submitting a huggingface model to neptune ai's model registry, run

```docker run \
    --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
    seb/keywords-base:latest \
    python -m src.register_base_model```

    #onclusiveml/keywords-train:latest \