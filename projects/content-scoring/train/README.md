# Overview

For details on how to run and maintain the `content-scoring` project `train` component, please refer
to the
- [the project README](../README.md) and
- [the project train doc.](../../doc/01_train.md)

using

- `PROJECT_NAME=content-scoring`, and
- `COMPONENT=train`

## Upload Pretrained Model
The `upload_pretrained_model.py` file is a temporary alternative to pushing a [specific model](https://s3.console.aws.amazon.com/s3/buckets/content-scoring-dev/content-scoring-workflow/model/) to neptune, skipping the training of the content-scoring model entirely. To achieve this:
- run `download_model.sh`
- run `make projects.start/content-scoring COMPONENT=train`
