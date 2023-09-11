# Internal libraries

Internal libraries implement abstractions that allow us to build our ML applications from a
consistent and maintainable ecosystem.

## Libraries

| Reference        | Upstream dependencies     | Description                                           | Target Hardware | Unit | Integration | Functional |
| ---------------- | --------------------------| ----------------------------------------------------- | --------------- | ---- | ----------- | ---------- |
| `core`           | n/a                       | Python base for core and project components           | cpu             |   x  |             |            |
| `tracking`       | `core`                    | Internal wrapper around `neptune` library             | cpu             |   x  |      x      |            |
| `serving`        |                           | Internal FastAPI-based serving library                | cpu             |   x  |      x      |      x     |
| `compile`        | `core`                    | Compilation utilities for `transformers` type models  | inf1            |   x  |             |      x     |
| `models`         | `compile`                 | Model classes to be used in project `serve` component | inf1, cpu       |   x  |      x      |      x     |
| `nlp`            | `core`                    | Cross project NLP utilities                           | cpu             |   x  |             |            |
| `syndicate`      | `nlp      `               | Cross project hashing utilities                       | cpu             |   x  |             |            |

## Dependency management

We use poetry to declare and pin python package and upstream library version dependencies. Each
library must ship with
- a `pyproject.toml` file declaring the dependencies
- an automatically created (`libs.lock` below)`poetry.lock` file showing resolved dependencies
- a `poetry.toml` file disabling the virtual environment creation in the Github Action CI

The CI flow implementing automated building and testing of all internal libraries is [`_libs.yaml`](../.github/workflows/_libs.yaml)

## Makefile Targets

We use a set of `make` targets to consistently execute the main library development tasks.

Available targets are:

```text
Available targets:

    libs.lock/<library>                     (Re-)writes a library's poetry lock file.
    libs.install/<library>                  Installs a library and dependencies locally
    libs.install-all                        Installs all libraries and dependencies locally
    libs.unit/<image>                       Runs unit tests for a library
    libs.unit-all                           Runs unit tests for all registered libraries
    libs.integration/<library>                Runs integration tests for a library
    libs.integration-all                    Runs integration tests for all registered libraries
    libs.functional/<library>                 Runs integration tests for a library*
    libs.functional-all                     Runs integration tests for all registered libraries*
    libs.test/<library>                       Runs the full test suite for a library*
    libs.test-all                           Runs the full test suite for all registered libraries*


```
* assumes *no* server <-> client test structure

For more details, see the [libs level `makefile`](./makefile.mk).

Note that some of the default values for `make` variables are defined in the
[repository level `makefile`](../Makefile)

## Useful commands

To (re-)write your library's lock file, run: `make libs.lock/${LIBRARY_NAME}`

To (re-)install your library locally, run: `make libs.install/${LIBRARY_NAME}`

To run your library's unit tests, run: `make libs.unit/${LIBRARY_NAME}`

To run your library's integration tests, run: `make libs.integration/${LIBRARY_NAME}`

To run your library's functional tests, run: `make libs.functional/${LIBRARY_NAME}`

For more documentation on a given library, see the individual library's dedicated `README.md`.

## Dependabot 

Add the updated component on the [dependabot config file](./../.github/dependabot.yaml)
