# LSH API - Locality-Sensitive Hashing

This repository contains an implementation of the LSH API, utilizing Locality-Sensitive Hashing to efficiently perform nearest neighbor search in high-dimensional spaces.

## Table of Contents

1. [Introduction](#introduction)
2. [Files](#files)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)

## Introduction

LSH (Locality-Sensitive Hashing) is a powerful technique used in data mining and machine learning to approximate nearest neighbor search in high-dimensional data. This repository provides an API implementation of LSH, allowing users to efficiently find similar items based on their content signatures.

## Files

The project is structured into the following files and directories:

- **src/app.py**: This file contains the FastAPI application setup and routing configuration for the LSH API.

- **src/settings.py**: The settings module defines the configuration for the LSH API, including API name, description, environment, and logging level.

- **src/schemas/request.py**: Contains the Pydantic schema for the request payload when making predictions.

- **src/schemas/response.py**: Contains the Pydantic schema for the response payload when making predictions.

- **src/routes/v1/lsh.py**: Defines the API endpoint `/lsh/predict`, which receives requests and returns LSH signatures for the input content.

- **src/predict/lsh.py**: Implements the LSH handler, which performs the core LSH operations such as shingling, generating LSH signatures, and preprocessing text data.

## Setup and Installation

To set up the LSH API and its dependencies, follow these steps:

1. Ensure you have Python 3.8.16 installed.

2. Install the required dependencies by running the following command:
```
make projects.lock/lsh COMPONENT=serve
```
This will update the poetry.lock if it is not the case already.
Essentially, the libraries you need to immport are mostly our custom librairies: core, nlp and syndicate.

3. Optionally, create a virtual environment to isolate the project dependencies.

## Usage

To use the LSH API, follow these steps:

1. Start the FastAPI server by running the following command from the ml-mesh directory:
```
make projects.build/lsh
make projects.start/lsh
```

2. The LSH API is now accessible at `http://localhost:8000`. You can interact with the API using your preferred HTTP client.

## API Endpoints

### Predict LSH Signature

**Endpoint**: `/lsh/predict`

**Method**: POST

**Request Payload**:

```json
{
  "content": "Sample content to generate LSH signature for.",
  "language": "en",
  "shingle_list": 5,
  "threshold": 0.6,
  "num_perm": 128,
  "weights": null
}
```
**Response Payload**:
```json
{
  "signature": "LSH signature for the input content."
}
```

## Syndicate library

As you noticed yourself, the syndicate library is essential to the functioning of the API. Thus I encourage to check it out at /ml-mesh/libs/syndicate
