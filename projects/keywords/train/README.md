# 'Train' a keybert huggingface model

To run the container step submitting a huggingface model to neptune ai's model registry, run

```docker run \
    --env NEPTUNE_API_TOKEN={neptune_ai_api_token_value_here} \
    onclusiveml/keywords-train:latest \
    python -m src.register_trained_model.py```