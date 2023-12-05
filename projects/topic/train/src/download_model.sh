#!/usr/bin/env bash
aws s3 cp s3://topic-detection-dev/bertopic-workflow/model/ model_artifacts/ --recursive
aws s3 cp s3://topic-detection-dev/TOPIC-TRAINED-43.parquet .
