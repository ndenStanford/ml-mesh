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

## low level dependencies
PYTHON_VERSION=$(shell cat .python-version)
PYTHON_SHORT_VERSION=$(shell grep -Eo '[0-9]\.[0-9]+' .python-version  | head -1)
POETRY_VERSION=$(shell cat .poetry-version)
PIP_VERSION=$(shell cat .pip-version)
SCALA_VERSION=$(shell cat .scala-version)
CUDA_VERSION=$(shell cat .cuda-version)
FLINK_VERSION=$(shell cat .flink-version)
BEAM_VERSION=$(shell cat .beam-version)
BEAM_SHORT_VERSION=$(shell grep -Eo '[0-9]\.[0-9]+' .beam-version  | head -1)
DASK_VERSION=$(shell cat .dask-version)
AWS_CLI_VERSION=$(shell cat .aws-cli-version)
S6_VERSION=$(shell cat .s6-version)
KUBECTL_VERSION=$(shell cat .kubectl-version)
JAVA_VERSION=$(shell cat .java-version)
NODE_VERSION=$(shell cat .node-version)

## VARIABLES
ifeq ($(USE_DOCKER_CACHE),false)
	DOCKER_FLAGS += --no-cache
endif


# all core docker images
ALL_DOCKER_IMGS:= \
	python-base \
	gpu-base \
	neuron-inference \
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
	hashing \
	training \
	llms

# libraries included in sonarqube coverage tests
COVERED_LIBS:= \
	compile \
	core \
	data \
	models \
	nlp \
	serving \
	tracking \
	hashing \
	llms

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
