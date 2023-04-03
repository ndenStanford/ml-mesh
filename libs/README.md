# Internal libraries

Internal libraries implement abstractions that allow us to build our ML applications from a consistent echosystem.

## Libraries

- **core**: base classes and global utilities used in all libraries and projects.
- **data**: dataset lifecycle management.
- **models**: model wrappers and parameter maangement.
- **neuron**: neuron reusable objects to compile models.
- **neptune**: Neptune.ai utilities.
- **nlp**: internal NLP utilities.
- **serving**: model wrappers for serving.
- **training**: object suite to enable training models at scale.

## Makefile Targets

```text
Available targets:

    libs.install                            Installs a library and dependencies locally
    libs.unit                               Runs unit tests for a library
    libs.integration                        Runs integration tests for a library
    libs.test                               Runs the full test suite
    libs.unit-all                           Runs unit tests for all registered libraries
    libs.integration-all                    Runs integration tests for all registered libraries
    libs.test-all                           Runs the full test suite for all registered libraries
    libs.install-all                        Installs all libraries and dependencies locally

```
