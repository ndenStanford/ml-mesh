# Overview

For details on how to run and maintain the `entity-linking` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/04_serve.md)

using

- `PROJECT_NAME=entity-linking`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:9000/entity-linking/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:9000/entity-linking/v1/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:9000/entity-linking/v1/predict' \
    -H 'Content-Type: application/json' \
    -d '{
        "data": {
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": {
                "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium."  # noqa
            },
            "parameters": {"lang": "en"},
        }
    }'
```

This should return a response along the lines of
```
{
    "version": 1,
    "data": {
        "identifier": None,
        "namespace": "entity-linking",
        "attributes": {
            "entities": [
                {
                    "entity_type": "ORG",
                    "entity_text": "Tottenham Hotspur Football Club",
                    "score": 0.9259419441223145,
                    "sentence_index": 0,
                    "wiki_link": "https://www.wikidata.org/wiki/Q18741",
                }
            ]
        },
    },
}
```

An invocation of the `predict` endpoint with invalid language specs...

```bash
curl -X 'POST' 'http://0.0.0.0:9000/entity-linking/v1/predict' \
    -H 'Content-Type: application/json' \
    -d '{
        "data": {
            "identifier": None,
            "namespace": "entity-linking",
            "attributes": {
                "content": "Irrelevant content because of invalid message value (nonsense)."
            },
            "parameters": {"lang": "invalid_language"},
        }
    }'
```

Will generate a `422` error code response describing the language lookup related issue in detail:

```
{
  "detail": [
    {
      "type": "json_invalid",
      "loc": [
        "body",
        39
      ],
      "msg": "JSON decode error",
      "input": {},
      "ctx": {
        "error": "Expecting value"
      }
    }
  ]
}
```
