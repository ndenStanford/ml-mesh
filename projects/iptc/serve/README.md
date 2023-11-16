# Overview

For details on how to run and maintain the `iptc` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/04_serve.md)

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
    -d ' {
                "data": {
                    "namespace": "iptc",
                    "attributes": {
                        "content": """Stocks reversed earlier losses to close higher despite rising oil prices
            that followed the attack by Hamas on Israel over the weekend. Dovish comments by
            Federal Reserve officials boosted the three major indexes. The Dow Jones Industrial
            Average added nearly 200 points."""
                    },
                    "parameters": {},
                }
            }'
```

This should return a response along the lines of
```bash
'   {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "iptc",
            "attributes": {
                "iptc": [
                    {
                        "label": "economy, business and finance",
                        "score": 0.9871
                    }
                ]
            },
        },
    }'
```
