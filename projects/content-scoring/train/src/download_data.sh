#!/usr/bin/env bash
aws s3 cp s3://content-scoring-dev/content-scoring-workflow/model/ projects/content-scoring/train/data/ --recursive
