# `Train Manual`

Replace <project_name> with "ner" or "sentiment"

`export PROJECT_NAME==?`

## 1 Overview

The `<project_name>-train` container image provides the code and runtime environment for retrieving a
specified feature extraction pipeline from huggingface and registering it on our internal neptun AI
model registry.

The python module implementing the above process is `register_trained_model.py`.

It draws its configurations from the `settings.py` module, which parses all required
environment variable either

- from the environment, or, if not specified,
- from the `config/dev.env` dotenv file (locally or in the container when running inside docker)

Specs defined in the `config/prod.env` is used only during CI processes.

## 2 Running the pipeline

### 2.1 Without containers

For development purposes, the pipeline can be run locally without containers.

1. Set the neptune authentication token value
   - `export NEPTUNE_API_TOKEN==?`
2. Change into the `projects/<project_name>/train/src` directory
   - `cd projects/<project_name>/train`
3. Run the model retrieval + registering step
   - `python -m src.register_trained_model`

As described in the previous section the `settings.py` script will fall back onto the
`config/dev.env` file for any environment variables that it cant obtain from the environment.
Editing that file allows for configuring development pipeline runs.

### 2.2 With containers

#### 2.2.1 Building the docker container

To locally build the image tagged as
`063759612765.dkr.ecr.us-east-1.amazonaws.com/<project_name>-train:latest`, run the `make` target:

```make
make projects.build/<project_name> \
  COMPONENT=train \
  ENVIRONMENT=dev
```
You can replace `latest` with `$IMAGE_TAG` if you would prefer to tag with a different name. Make sure you've exported a value for `$IMAGE_TAG`

#### 2.2.2 Running the components inside docker

1. Export run environment variables

   - `export NEPTUNE_API_TOKEN=?`
   - `export PATH_TO_REPOSITORY=?`

2. Update the `dev.env` file in the `config` directory as needed. We will inject environment
   variable values directly from the file into the running container (see below) to allow for
   pipeline runtime configurations without requiring a rebuild of the docker container.

3. Run the container:

You can run the command with this command (which uses docker compose):

```
make projects.start/<project_name> COMPONENT=train
```

Or run this docker command:

```docker
docker run \
  --env NEPTUNE_API_TOKEN=$NEPTUNE_API_TOKEN \
  -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
  -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
  --env-file $PATH_TO_REPOSITORY/projects/<project_name>/train/config/dev.env \
  -t 063759612765.dkr.ecr.us-east-1.amazonaws.com/<project_name>-train:latest \
  python -m src.register_trained_model
```

If you're using a different tag e.g. `$IMAGE_TAG`, make sure to replace `latest` with it.

- Note: If the `--env-file` command is omitted in the docker command,
  the pipeline will fall back on the default values defined in the `settings.py` file.
