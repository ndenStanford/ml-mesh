# Overview

For details on how to run and maintain the `ner` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/03_serve.md)

using

- `PROJECT_NAME=ner`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/model/ner/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/v1/model/ner/predict' -H 'Content-Type: application/json' -d '{"configuration": {"return_pos": true, "language": "en"}, "inputs": {"content": "Google is cool"}}'
```

This should return a response along the lines of
```bash
{"outputs":{"predicted_content":[{"entity_type":"ORG","entity_text":"Google","score":0.9729547,"sentence_index":0,"start":0,"end":6}]}}
```
