# Overview

For details on how to run and maintain the `gch-summarization` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../docs/04_serve.md)

using

- `PROJECT_NAME=gch-summarization`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/gch-summarization/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/gch-summarization/v1/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/gch-summarization/v1/predict' -H 'Content-Type: application/json' -d '{"configuration": {"language": "en"}, "inputs": {"content":
"Sky News announces slate of special programming for the appointment of the UK's new Prime Minister.\nSky News' political programming will expand ahead of a momentous week in UK politics with the impending announcement of the new Prime Minister. Sky News' key political programmes will return to bring audiences in-depth discussion and analysis of all the latest news with live coverage from Downing Street and Westminster.\nHead of Sky News, John Ryley:\n'This is a momentous week in British politics, where a new Prime Minister will take on an in-tray bursting with crunch decisions."}}'
```

This should return a response along the lines of
```bash
{
  "version": 1,
  "data": {
    "identifier": null,
    "namespace": "gch-summarization",
    "attributes": {
      "summary": "Sky News to expand political programming ahead of the appointment of the new Prime Minister. Key political programmes will return to bring audiences in-depth discussion and analysis."}
      },
```
