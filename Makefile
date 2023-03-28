## VARIABLES
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
DOCKER_EXTRA_FLAGS?=
DOCKER_CMD?=
DOCKER_STAGE?=production
USE_DOCKER_CACHE?=false
WITH_DOCKER?=false
PORT?=8888
ENVIRONMENT?=ci

##  DOCKER EXTRA FLAGS
ifeq ($(USE_DOCKER_CACHE),true)
	DOCKER_EXTRA_FLAGS += --cache-from $(OWNER)/$(notdir $@)-$(COMPONENT):$(IMAGE_TAG)
else
	DOCKER_EXTRA_FLAGS += --no-cache
endif

ifeq ($(DOCKER_STAGE),development)
	DOCKER_EXTRA_FLAGS += --target development
endif

ifeq ($(DOCKER_STAGE),production)
	DOCKER_EXTRA_FLAGS += --target production
endif

ifeq ($(WITH_DOCKER), true)
	DOCKER_CMD += docker-compose -f ../docker-compose.$(ENVIRONMENT).yaml run --service-ports $(COMPONENT)
endif

## VARIABLES

# all core docker images
ALL_DOCKER_IMGS:= \
	python-base \
	neuron-compile \
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
	@find . -name '.cache' -exec rm -rf {} \;
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
