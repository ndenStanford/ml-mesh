#!/bin/bash
aws s3 cp s3://sagemaker-training-result/model_dir/00000000/model.pt models/
aws s3 cp s3://sagemaker-training-result/tokenizer.vocab models/
