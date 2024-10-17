# Overview

For details on how to run and maintain the `visitor-estimation` project `serve` component, please refer
to the
- [the project README](../README.md) and
- [the project serve doc.](../../../docs/04_serve.md)

using

- `PROJECT_NAME=visitor-estimation`, and
- `COMPONENT=serve`

# Invoking the model service

To invoke the `live` endpoint for server liveness, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/live'
```

To invoke the `bio` endpoint for model meta data, use:

```bash
curl -X 'GET' 'http://0.0.0.0:8000/v1/visitor-estimation/bio'
```

To invoke the `predict` endpoint for inference, use:

```bash
curl -X 'POST' 'http://0.0.0.0:8000/v1/visitor-estimation/predict' \
    -H 'Content-Type: application/json' \
    -d '{"data": {
            "namespace": "sentiment",
            "attributes": {
                "input": [
                    {
                        "profileID": 2252,
                        "analyticsTimestamp": [
                            "2016-08-12T00:00:00",
                            "2016-08-11T00:00:00",
                            "2016-08-13T00:00:00",
                        ],
                        "entityTimestamp": "2016-08-10T07:46:59",
                        "social": {
                            "metadataTimestamp": [
                                "2016-08-11T00:00:00",
                                "2016-08-11T18:00:00",
                                "2016-08-12T10:00:00",
                            ],
                            "fbLikes": [1000, 1000, 1000],
                            "fbComments": [1000, 1000, 1000],
                            "fbTotal": [1000, 1000, 1000],
                            "fbShares": [1000, 1000, 1000],
                            "linkedInShares": [1000, None, 1000],
                            "googlePlusones": [1000, None, 1100],
                            "twitterRetweets": [1000, 1000, 1200],
                        },
                        "wordCount": 500,
                        "domainLinkCount": 2,
                        "nonDomainLinkCount": 0,
                        "namedEntityCount": 3,
                        "relevance": 0.92,
                        "pagerank": 7.3,
                        "companySectorId": 10,
                        "typeCd": 3,
                        "category": 2,
                        "isSyndicateChild": False,
                        "isSyndicateParent": True,
                    }
                ],
            },
        }
    },'
```

This should return a response along the lines of
```bash
{
    "version": 1,
    "data": {
        "identifier": None,
        "namespace": "visitor-estimation",
        "attributes": {
            "predicted_visitors": 1,
        },
    },
},
```
