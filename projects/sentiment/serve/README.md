# Overview

For details on how to run and maintain the `sentiment` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../../docs/04_serve.md)

using

- `PROJECT_NAME=sentiment`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v2/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v2/model/sentiment/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/v2/model/sentiment/predict' \
    -H 'Content-Type: application/json' \
    -d '{
        "data": {
            "namespace": "sentiment",
            "attributes": {
                "content": "London is a wonderful city. John is a terrible man.",
                "entities": [
                    {
                        "entity_type": "LOC",
                        "entity_text": "London",
                        "score": "0.99966383",
                        "sentence_index": 0,
                        "start": 0,
                        "end": 6,
                    },
                    {
                        "entity_type": "PER",
                        "entity_text": "John",
                        "score": "0.9991505",
                        "sentence_index": 1,
                        "start": 0,
                        "end": 4,
                    },
                ],
            },
            "parameters": {
                "language": "en",
            },
        }
    },'
```

This should return a response along the lines of
```bash
'   {
        "version": 2,
        "data": {
            "identifier": None,
            "namespace": "sentiment",
            "attributes": {
                "label": "negative",
                "negative_prob": 0.9142,
                "neutral_prob": 0.0578,
                "positive_prob": 0.0280,
                "entities": [
                    {
                        "entity_type": "LOC",
                        "entity_text": "London",
                        "score": 0.99966383,
                        "sentence_index": 0,
                        "start": 0,
                        "end": 6,
                        "sentiment": "positive",
                    },
                    {
                        "entity_type": "PER",
                        "entity_text": "John",
                        "score": 0.9991505,
                        "sentence_index": 1,
                        "start": 0,
                        "end": 4,
                        "sentiment": "negative",
                    },
                ],
            },
        },
    },
```
