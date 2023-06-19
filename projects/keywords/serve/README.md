# Overview

The `serve` image implements both the ML `keywords` model serving application as well as all
accompanying test suites as defined in [the post model regsitry flow of the continuous integration
design for ML serving images](https://onclusive01-my.sharepoint.com/:w:/r/personal/sebastian_scherer_onclusive_com/Documents/RFC%20-%20ML%20CI%20pipeline%20framework.docx?d=w74da3073c12b412a9f8b8acd8f741dbe&csf=1&web=1&e=mJXG6p).

## Serving the `keywords` model

### Configuring the model server

The keywords model server is implemented using the internal `serving` library. To configure it, you
should use its `KeywordsServingParams` class in the `keywords_serving_params` module as the
designated for configuration environment variables. These inlcude

- `KeywordsServedModelParams`
  - model artifact location on local disk of serving node
  - model serving logic parametrization
- `UvicornSettings`
  - a uvicorn configuration](<https://github.com/encode/uvicorn/blob/master/uvicorn/config.py>) specification; serving process configuration - see the `serving` library documentation for details

### Running the model server

To run the model server:

- make sure you are in the `/projects/keywords/serve` directory
- run `uvicorn src.keywords_model_server:keywords_model_server --reload`
