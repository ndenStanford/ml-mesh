# LSH API - LOCALITY-SENSITIVE HASHING

This repository contains an implementation of the Topic Detection API, utilizing GPT to efficiently perform deep analysis to some given aspects of a group of documents.

## Table of Contents

1. [Usage](#usage)
2. [API Endpoints](#api-endpoints)


## Usage

To use the Topic-Detection API, follow these steps:

1. Start the FastAPI server by running the following command from the ml-mesh directory:
```
make projects.build/topic-detection
make projects.start/topic-detection
```

2. The Topic-Detection API is now accessible at `http://localhost:8888`. You can interact with the API using your preferred HTTP client.

## API Endpoints

### Predict LSH Signature

**Endpoint**: `/topic-detection/predict`

**Method**: POST
