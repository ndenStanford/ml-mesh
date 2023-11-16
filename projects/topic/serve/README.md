# Overview

For details on how to run and maintain the `topic` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/04_serve.md)

using

- `PROJECT_NAME=topic`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/model/topic/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/v1/model/topic/predict' \
    -H 'Content-Type: application/json' \
    -d '{ "data": { "namespace": "topic", "attributes": { "text": "London is a wonderful city. John is a terrible man.", }, "parameters": { "language": "en", }, } }'
```

This should return a response along the lines of
```bash
{ "version": 1, "data": { "identifier": None, "namespace": "topic", "attributes": {"topic_id": "861"}, }, }
```
