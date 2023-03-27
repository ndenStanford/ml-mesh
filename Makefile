SHELL := /bin/bash
PWD   = $(shell pwd)
AWS_REGION?=us-east-1
AWS_ACCOUNT_ID?=063759612765
# NOTE: the AWS ECR owner name is: $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
OWNER?=onclusiveml
PLATFORM?=linux/amd64
COMPONENT?=serve
DEBUG?=true
IMAGE_TAG?=latest
TARGET_BUILD_STAGE?=production

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
	core

# all projects
ALL_PROJECTS:= \
	keybert

## SUBFOLDER MAKEFILES
include libs/makefile.mk
include docker/makefile.mk
include projects/makefile.mk


## COMMON TARGETS

.PHONY: clean

clean: ## Clean build artifacts.
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name '.pytest_cache' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov

install:
	poetry install

help:
	@echo "WIP"

upgrade-python:
	@echo "WIP"
