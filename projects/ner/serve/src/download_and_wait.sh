#!/bin/bash
echo 'Starting ner model download process'
python -m src.download
echo 'Finished ner model download process. Sleeping for 10 minutes to wait for entity linking download to complete'
sleep 20m
