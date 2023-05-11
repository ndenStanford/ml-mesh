docker.build/%: docker.set ## Build app
	@echo "::group::Build$(notdir $@) (system architecture)"
	docker compose -f ./docker/docker-compose.yaml build $(notdir $@) --no-cache
	@echo "::endgroup::"

docker.deploy/%: docker.set ## Deploy project IMAGE docker image to ECR.
	docker compose -f ./docker/docker-compose.yaml push $(notdir $@)

docker.validate/%: docker.set ## Validate core docker image build
	docker compose -f docker/docker-compose.yaml run $(notdir $@)-tests

docker.lock/%:
	poetry lock --directory=docker/$(notdir $@)

docker.set:
	export IMAGE_TAG=$(IMAGE_TAG)
	export TARGET_BUILD_STAGE=$(TARGET_BUILD_STAGE)
	export AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID)

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
