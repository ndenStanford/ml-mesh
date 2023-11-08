# ML projects

This folder contains the implementation of all our machine learning projects. Each project is split
 into a maximum of 5 components:

- ingest
- register
- train
- compile
- serve

## Projects


| Project                                                                                           | Owner                               | Reference           | Description                                  | Data Type | Ingest | Register | Train | Compile | Serve |
|---------------------------------------------------------------------------------------------------|-------------------------------------|---------------------|----------------------------------------------| --------- |--------| -------- | ----- | ------- | ---- |
| [IPTC](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3192815811/IPTC)                      | <jian.tong@onclusive.com>           | `iptc`              | Document topic classification                | Text      | x      |     x    |   x   |         |      |
| [Sentiment](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3192815818/Sentiment)            | <nutchapol.dendumrongsup@onclusive.com> | `sentiment`         | Document Sentiment classification            | Text      |        |          |   x   |    x    |   x  |
| [Keywords](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3208904707/Keybert)               | <sebastian.scherer@onclusive.com>   | `keywords`          | Keyword extractions from text                | Text      |        |          |   x   |    x    |   x  |
| [NER](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3192652408/Entity)                     | <syed.reza@onclusive.com>           | `ner`               | Named Entity Recognition                     | Text      |        |          |   x   |    x    |   x  |
| [LSH](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3357573656/Syndicate+Detection)        | <amaury.deguillebon@onclusive.com>  | `lsh`               | LSH                                          | Text      |        |          |  n/a  |   n/a   |   x  |
| Summarization                                                                                     | <nutchapol.dendumrongsup@onclusive.com> | `summarization`     | Summarization for Analyst with OpenAI's GPT  | Text      |        |          |       |         |   x* |
| GCH-Summarization                                                                                 | <zheyuan.hu@onclusive.com>          | `gch-summarization` | Summarization for GCH with Pretrained Models | Text      |        |          |   x   |    x    |   x* |
| [Entity linking](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3192815790/Entity+Linking)  | <rene-jean.corneille@onclusive.com> | `entity-linking`    | Entity linking                               | Text      |        |          |       |         |   x* |
| [Topic Detection](https://onclusive.atlassian.net/wiki/spaces/ML/pages/3357311714/Topic+Trend+Detection) | <vishal.singh@onclusive.com>        | `topic`             | Topic Detection                              | Text      | x      |          |       |         |     |


Note: x* - denotes a serving component that hasn't been migrated to the `serving` library yet

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
