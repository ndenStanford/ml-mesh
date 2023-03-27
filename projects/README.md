# ML projects

This folder contains the implmentation of all our machine learning projects. Each project is split into a maximum of 5 components:

- prepare
- train
- compile
- serve
- backfill

##  Projects

| Project       | Description                       | Data Type | Prepare | Train | Compile | Serve |
| ------------- | --------------------------------- | --------- | ------- | ----- | ------- | ----- | --- |
| IPTC          | Document topic classification     | Text      |         |       |         |       |     |
| Sentiment     | Document Sentiment classification | Text      |         |       |         |       |     |
| Keybert       | Keyword extractions from text     | Text      |         |       |         |       | x   |
| Summarization | Text summarization                | Text      |         |       |         |       | x   |

- **keybert**: keyword extraction

## Makefile Targets

```text
Available targets:

    projects.build                      Builds the component docker image
    projects.install                    Install component dependencies locally
    projects.deploy                     Deploys component docker image to ECR
    projects.tag                        Tags component image
    projects.untag                      Untags component image
    projects.start                      Start development container for component
    projects.test                       Runs component full test suite
    projects.unit                       Runs component unit test
    projects.integration                Runs component integration test
    projects.lock                       Updates the poetry lock file

```
