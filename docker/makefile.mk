docker.build/%: docker.set ## Build app
	@echo "::group::Build$(notdir $@) (system architecture)"
	docker compose -f ./docker/docker-compose.$(ENVIRONMENT).yaml build $(notdir $@) $(DOCKER_FLAGS) \
			--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
			--build-arg PYTHON_SHORT_VERSION=$(PYTHON_SHORT_VERSION) \
			--build-arg PIP_VERSION=$(PIP_VERSION) \
			--build-arg POETRY_VERSION=$(POETRY_VERSION) \
			--build-arg SCALA_VERSION=$(SCALA_VERSION) \
			--build-arg CUDA_VERSION=$(CUDA_VERSION) \
			--build-arg FLINK_VERSION=$(FLINK_VERSION) \
			--build-arg BEAM_VERSION=$(BEAM_VERSION) \
			--build-arg DASK_VERSION=$(DASK_VERSION) \
			--build-arg AWS_CLI_VERSION=$(AWS_CLI_VERSION) \
			--build-arg S6_VERSION=$(S6_VERSION) \
			--build-arg KUBECTL_VERSION=$(KUBECTL_VERSION) \
			--build-arg JAVA_VERSION=$(JAVA_VERSION) \
			--build-arg NODE_VERSION=$(NODE_VERSION) \
			--build-arg UBUNTU_VERSION=$(UBUNTU_VERSION)

	@echo "::endgroup::"

docker.start/%: ## run a bash in interactive mode
	docker compose -f ./docker/docker-compose.$(ENVIRONMENT).yaml up $(notdir $@) --force-recreate

docker.stop/%: ## run a bash in interactive mode
	docker compose -f ./docker/docker-compose.$(ENVIRONMENT).yaml down --remove-orphans

docker.deploy/%: docker.set ## Deploy project IMAGE docker image to ECR.
	docker compose -f ./docker/docker-compose.$(ENVIRONMENT).yaml push $(notdir $@)

docker.validate/%: docker.set ## Validate core docker image build
	docker compose -f docker/docker-compose.$(ENVIRONMENT).yaml up $(notdir $@)-tests --exit-code-from $(notdir $@)-tests --force-recreate

docker.lock/%:
	poetry lock --directory=docker/$(notdir $@)

docker.set:
	export IMAGE_TAG=$(IMAGE_TAG)
	export TARGET_BUILD_STAGE=$(TARGET_BUILD_STAGE)
	export AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID)
	export DEPLOYMENT=$(DEPLOYMENT)

docker.build-all: $(foreach I, $(ALL_DOCKER_IMGS), docker.build/$(I)) ## build all images

docker.cont-clean-all: docker.cont-stop-all docker.cont-rm-all ## clean all containers (stop and remove)
docker.cont-stop-all: ## stop all containers
	@echo "Stopping all containers  ..."
	-docker stop -t0 $(shell docker ps -a -q) 2> /dev/null

docker.cont-rm-all: ## Remove all containers
	@echo "Removing all containers ..."
	-docker rm --force $(shell docker ps -a -q) 2> /dev/null

docker.img-rm-all: ## remove jupyter images
	@echo "Removing $(OWNER) images ..."
	-docker rmi --force $(shell docker images --quiet "$(OWNER)/*") 2> /dev/null

docker.clean: docker.rm-deps-all docker.cont-clean-all docker.img-rm-all ## clean environment

docker.login: ## login
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
