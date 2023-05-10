# ML projects

This folder contains the implmentation of all our machine learning projects. Each project is split into a maximum of 5 components:

- ingest
- prepare
- train
- compile
- serve

## Projects

| Project       | Description                       | Data Type | Prepare | Train | Compile | Serve |     |
| ------------- | --------------------------------- | --------- | ------- | ----- | ------- | ----- | --- |
| IPTC          | Document topic classification     | Text      |         |       |         |       |     |
| Sentiment     | Document Sentiment classification | Text      |         |       |         |       |     |
| Keywords      | Keyword extractions from text     | Text      |         |       |         |       | x   |
| Summarization | Text summarization                | Text      |         |       |         |       | x   |

- **keybert**: keyword extraction

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
    projects.lock/<project>                     Updates the poetry lock file. Variable(s): COMPONENT.

```
