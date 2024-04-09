# Overview

For details on how to run and maintain the `topic` project `train` component, please refer
to the
- [the project README](../README.md) and
- [the project train doc.](../../docs/02_train.md)

using

- `PROJECT_NAME=topic`, and
- `COMPONENT=train`

## Upload Pretrained Model
The `upload_pretrained_model.py` file is a temporary alternative to pushing a [specific model](https://s3.console.aws.amazon.com/s3/buckets/topic-detection-dev?region=us-east-1&prefix=bertopic-workflow/model/&showversions=false) to neptune, skipping the training of the bertopic model entirely. To achieve this:
- run `download_model.sh`
- replace `command: [python, -m, src.train_model]` found in [docker-compose-dev.yaml](../docker-compose.dev.yaml#L78) with `command: [python, -m, src.upload_pretrained_model]`
- run `make projects.start/topic COMPONENT=train`
