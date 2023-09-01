# ML projects

This folder contains the implementation of all our machine learning projects. Each project is split
 into a maximum of 5 components:

- ingest
- prepare
- train
- compile
- serve

## Projects

| Project       | Reference       | Description                       | Data Type | Prepare | Train | Compile | Serve |     |
| ------------- | --------------- | --------------------------------- | --------- | ------- | ----- | ------- | ----- | --- |
| IPTC          | n/a             | Document topic classification     | Text      |         |       |         |       |     |
| Sentiment     | `sentiment`     | Document Sentiment classification | Text      |         |       |    x    |       |     |
| Keywords      | `keywords`      | Keyword extractions from text     | Text      |         |   x   |    x    |   x   | x   |
| Summarization | `summarization` | Text summarization                | Text      |         |       |         |       | x   |
| NER           | `ner`           | Named Entity Recognition          | Text      |         |  n/a  |   n/a   |   x   | x   |


## Makefile Targets

```text
Available targets:

    projects.build/<project>                    Builds the component docker image. Variable(s): COMPONENT, ENVIRONMENT.
    projects.install/<project>                  Install component dependencies locally. Variable(s): COMPONENT
    projects.deploy/<project>                   Deploys component docker image to ECR. Variable(s): COMPONENT, ENVIRONMENT.
    projects.start/<project>                    Start development container for component. Variable(s): COMPONENT, ENVIRONMENT.
    projects.stop/<project>                     Stop development container for component. Variable(s): COMPONENT, ENVIRONMENT.
    projects.test/<project>                     Runs component full test suite. Variable(s): COMPONENT, ENVIRONMENT.
    projects.unit/<project>                     Runs component unit test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.integration/<project>              Runs component integration test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.functional/<project>               Runs component functional test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.load/<project>                     Runs component load test. Variable(s): COMPONENT, ENVIRONMENT.
    projects.compile/<project>                  Runs compile component pipeline step.Variable(s): PIPELINE_COMPONENT, ENVIRONMENT.
    projects.lock/<project>                     Updates the poetry lock file. Variable(s): COMPONENT.

```

## Manuals

The following component-specific manuals are available:
- [train](https://github.com/AirPR/ml-mesh/tree/develop/manuals/projects/01_train.md)
- [compile](https://github.com/AirPR/ml-mesh/tree/develop/manuals/projects/02_compile.md)
- [serve](https://github.com/AirPR/ml-mesh/tree/develop/manuals/projects/03_server.md)
