# Overview

List of the use case for this component:
- You provide a content, no target language, with translation = False -> you will have the language of the content detected.
- You provide a content, a target language, with translation = True -> you will have the language of the content detected, and your text will be translated into the target language, subject to if the language is part supported.
- You provide a source language -> you overwrite the language detection process.

For details on how to run and maintain the `translation` project `serve` component, please refer
to the
- [the project serve doc.](../../../docs/04_serve.md)

using

- `PROJECT_NAME=translation`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/translation/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/translation/v1/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/translation/v1/predict' \
    -H 'Content-Type: application/json' \
    -d '{
        "data": {
            "identifier": None,
            "namespace": "translation",
            "attributes": {
                "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium."  # noqa
            },
            "parameters": {
                "target_language": "fr",
                "translation": True,
            },
        }
    }'
```

This should return a response along the lines of
```
{
    "version": 1,
    "data": {
        "identifier": None,
        "namespace": "translation",
        "attributes": {
            "source_language": "en",
            "target_language": "fr",
            "translatedtext": "Le Tottenham Hotspur Football Club a élaboré des plans pour des appartements étudiants sur le site d'une ancienne imprimerie à proximité de son stade.",  # noqa
        },
    },
}
```

An invocation of the `predict` endpoint with invalid language specs...

```bash
curl -X 'POST' 'http://0.0.0.0:8000/translation/v1/predict' \
    -H 'Content-Type: application/json' \
    -d '{
        "data": {
            "identifier": None,
            "namespace": "translation",
            "attributes": {
                "content": "Tottenham Hotspur Football Club has drawn up plans for student flats on the site of a former printworks near its stadium."  # noqa
            },
            "parameters": {
                "source_language": ""
                "target_language": "fr",
                "translation": True,
            },
        }
    }'
```

Will generate a `204` error code response describing the language lookup related issue in detail:

```
"The language reference 'invalid language' could not be mapped, or the language could not be inferred from the content."
```
