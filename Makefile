## VARIABLES

PWD=$(shell pwd)
AWS_REGION?=us-east-1
AWS_ACCOUNT_ID?=690763002009
OWNER?=onclusiveml
PLATFORM?=linux/amd64
COMPONENT?=serve
DEBUG?=true
IMAGE_TAG?=latest
TARGET_BUILD_STAGE?=development
USE_DOCKER_CACHE?=false
WITHOUT_DOCKER?=false
START_CMD?=
UNIT_TEST_CMD?=
DOCKER_FLAGS?=
PORT?=8888
ENVIRONMENT?=dev

## VARIABLES
ifeq ($(USE_DOCKER_CACHE),false)
	DOCKER_FLAGS += --no-cache
endif

# all core docker images
ALL_DOCKER_IMGS:= \
	python-base \
	gpu-base \
	gpu-train \
	neuron-compile \
	neuron-inference \
	fastapi-serve \
	kubeflow-jupyter \
	kubeflow-torch-cpu \
	kubeflow-torch-gpu \
	kubeflow-torch-inf \
	kubeflow-data-science \
	dask-base

# all python libraries
ALL_LIBS:= \
	compile \
	core \
	data \
	models \
	nlp \
	serving \
	tracking \
	hashing

# all projects
ALL_PROJECTS:= \
	keywords \
	summarization \
	entity-linking \
	ner \
	iptc \
	lsh

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
