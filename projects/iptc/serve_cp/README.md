# Overview

For details on how to run and maintain the `iptc` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/03_serve.md)

using

- `PROJECT_NAME=iptc`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/model/iptc/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/v1/model/iptc/predict' \
    -H 'Content-Type: application/json' \
    -d '{"inputs": {"content": "London is a nice city."}, "configuration": {"language": "en", "entities": [{"entity_type": "LOC", "text": "London", "score": "0.9997141", "sentence_index": 0}]}}'
```

This should return a response along the lines of
```bash
{"outputs":{"label":"positive","negative_prob":0.0207,"positive_prob":0.9209,"entities":[{"entity_type":"LOC","text":"London","score":0.9997141,"sentence_index":0,"start":null,"end":null,"iptc":"positive"}]}}
```
