# Overview

The `keywords-compile` container image provides the runtime environment for all 4 components of the
**model compilation** segment of [the CI pipeline outlined in this RFC](https://onclusive01-my.sharepoint.com/:w:/g/personal/sebastian_scherer_onclusive_com/EXMw2nQrwSpBn4uKzY90Hb4BBFq1NHsYByDAo9-uc83iLg?e=B9ULGd):

1. download uncompiled model (either `base` or `trained`)
2. compile model (either `generic` or `neuron` torchscript tracing)
3. validate compiled model
4. registering compiled model on neptune AI

# Running the keywords model compile pipeline

Each of the 4 components corresponds to a python module:

1. `download_uncompiled_model.py`
2. `compile_model.py`
3. `validate_compiled_model.py`
4. `upload_compiled_model.py`

Each module draws its configurations from the `settings.py` module and the parameters defined there using `pydantic`. This allows for easy configuration of the flow via environment variables fed directly by Github Actions, without the need of an additional command line argument layer.

Orchestration of these components into the model compile pipeline is done by Github Actions of this same `ml-mesh` repository (as opposed to all other orchestration happening in `ml-platform`). The [modeol compile workflow can be found here](#add-link-here)