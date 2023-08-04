## VARIABLES

PWD=$(shell pwd)
AWS_REGION?=us-east-1
AWS_ACCOUNT_ID?=063759612765
OWNER?=onclusiveml
PLATFORM?=linux/amd64
COMPONENT?=serve
DEBUG?=true
IMAGE_TAG?=latest
TARGET_BUILD_STAGE?=development
USE_DOCKER_CACHE?=false
WITH_DOCKER?=false
PORT?=8888
ENVIRONMENT?=dev

## VARIABLES

# all core docker images
ALL_DOCKER_IMGS:= \
	python-base \
	neuron-compile \
	neuron-inference \
	fastapi-serve \
	kubeflow-jupyter \
	kubeflow-torch-cpu \
	kubeflow-data-science

# all python libraries
ALL_LIBS:= \
	compile \
	core \
	models \
	nlp \
	serving \
	tracking

# all projects
ALL_PROJECTS:= \
	keywords \
	summarization \
	entity-linking \
	ner

## SUBFOLDER MAKEFILES
include apps/makefile.mk
include libs/makefile.mk
include docker/makefile.mk
include projects/makefile.mk

## COMMON TARGETS

.PHONY: clean

clean: ## Clean build artifacts.
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name '.pytest_cache' -exec rm -rf {} \;
	@find . -name '.cache' -exec rm -rf {} \;
	@find . -name 'node_modules' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -r ~/.cache/*

install:
	poetry install

help:
	@echo "WIP"

upgrade-python:
	@echo "WIP"
