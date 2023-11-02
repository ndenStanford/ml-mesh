# ML projects

This folder contains the implementation of all our machine learning projects. Each project is split
 into a maximum of 5 components:

- ingest
- register
- train
- compile
- serve

## Projects


| Project          | Reference          | Description                                 | Data Type | Prepare | Train | Compile | Serve |
| ---------------- | ------------------ | ------------------------------------------- | --------- | ------- | ----- | ------- | ----- |
| IPTC             | `iptc`             | Document topic classification               | Text      |         |   x   |         |       |
| Sentiment        | `sentiment`        | Document Sentiment classification           | Text      |         |   x   |    x    |   x   |
| Keywords         | `keywords`         | Keyword extractions from text               | Text      |         |   x   |    x    |   x   |
| NER              | `ner`              | Named Entity Recognition                    | Text      |         |   x   |    x    |   x   |
| LSH              | `lsh`              | LSH                                         | Text      |         |  n/a  |   n/a   |   x   |
| Summarization    | `summarization`    | Summarization for Analyst with OpenAI's GPT | Text      |         |       |         |   x*  |
| GCH-Summarization| `gch-summarization`| Summarization for GCH with Pretrained Models| Text      |         |   x   |    x    |   x*  |
| Entity linking   | `entity-linking`   | Entity linking                              | Text      |         |       |         |   x*  |


Note: x* - denotes a serving component that hasnt been migrated to the `serving` library yet

## Makefile Targets & Docker-Compose Services

We use a set of `make` targets to consistently call `docker compose` services declared in
- the given project's development `docker-compose.dev.yaml` and
- the given project's CI `docker-compose.ci.yaml`

files, respectively.

Available targets are:

```text

    projects.build/<project>                    Builds the component docker image. Variable(s): COMPONENT, ENVIRONMENT.
    projects.install/<project>                  Install component dependencies locally. Variable(s): COMPONENT
    projects.deploy/<project>                   Deploys component docker image to ECR. Variable(s): COMPONENT, ENVIRONMENT.
    projects.start/<project>                    Start main task of development container for component. Variable(s): COMPONENT, ENVIRONMENT.
    projects.run/<project>                      Start auxiliary task of development container for component. Variable(s): COMPONENT, ENVIRONMENT, TASK.
    projects.stop/<project>                     Stop development container for component. Variable(s): COMPONENT, ENVIRONMENT.
    projects.test/<project>                     Runs component full test suite. Variable(s): COMPONENT, ENVIRONMENT.
    projects.unit/<project>                     Runs component unit test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.integration/<project>              Runs component integration test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.functional/<project>               Runs component functional test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.load/<project>                     Runs component load test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.compile/<project>                  Runs compile component pipeline step.Variable(s): PIPELINE_COMPONENT, ENVIRONMENT.
    projects.lock/<project>                     Updates the poetry lock file. Variable(s): COMPONENT.

```

For more details, see the [project level `makefile`](./makefile.mk).

Note that some of the default values for `make` variables are defined in the
[repository level `makefile`](../Makefile)

## Useful commands

The following component-specific in-depth docs are available:
- [train](./docs/01_train.md)
- [compile](./docs/02_compile.md)
- [serve](./docs/03_serve.md)

## Dependabot

Add the updated component on the [dependabot config file](./../.github/dependabot.yaml)
