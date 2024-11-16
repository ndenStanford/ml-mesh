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
            "namespace": "visitor-estimation",
            "attributes": {
                "input": [
                            {
                                "profile_id": 2252,
                                "analytics_timestamp": [
                                    "2016-08-12T00:00:00",
                                    "2016-08-11T00:00:00",
                                    "2016-08-13T00:00:00",
                                ],
                                "entity_timestamp": "2016-08-10T07:46:59",
                                "social": {
                                    "metadata_timestamp": [
                                        "2016-08-11T00:00:00",
                                        "2016-08-11T18:00:00",
                                        "2016-08-12T10:00:00",
                                    ],
                                    "fb_likes": [1000, 1000, 1000],
                                    "fb_comments": [1000, 1000, 1000],
                                    "fb_total": [1000, 1000, 1000],
                                    "fb_shares": [1000, 1000, 1000],
                                    "linkedIn_shares": [1000, None, 1000],
                                    "google_plusones": [1000, None, 1100],
                                    "twitter_retweets": [1000, 1000, 1200],
                                },
                                "word_count": 500,
                                "domain_link_count": 2,
                                "non_domain_link_count": 0,
                                "named_entity_count": 3,
                                "relevance": 0.92,
                                "page_rank": 7.3,
                                "company_sector_id": 16,
                                "type_cd": 3,
                                "category": 2,
                                "is_syndicate_child": False,
                                "is_syndicate_parent": True,
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
