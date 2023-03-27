docker.build/%: DOCKER_BUILD_ARGS?=
docker.build/%: ## build the latest image for a stack using the system's architecture
	@echo "::group::Build $(OWNER)/docker/$(notdir $@) (system architecture)"
		
	@docker build $(DOCKER_BUILD_ARGS) ./docker/$(notdir $@)	\
			-t $(OWNER)/$(notdir $@):${IMAGE_TAG} \
			-f ./docker/$(notdir $@)/Dockerfile	\
			--build-arg OWNER="$(OWNER)" --build-arg IMAGE_TAG="$(IMAGE_TAG)" --platform=$(PLATFORM) --target $(TARGET_BUILD_STAGE)

	@echo -n "built image size:"
	@docker images $(OWNER)/docker/$(notdir $@):latest --format "{{.Size}}"
	@echo "::endgroup::"

docker.run/%: ## run the specified image with optional command

	@echo "::group::Running image $(OWNER)/$(notdir $@):${IMAGE_TAG} as container ..."

	@docker run $(DOCKER_RUN_ARGS) \
		-t $(OWNER)/$(notdir $@):${IMAGE_TAG} \
		$(DOCKER_RUN_CMD)

	@echo "Completed running of image $(OWNER)/$(notdir $@):${IMAGE_TAG} as container."
	@echo "::endgroup::"

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

docker.pull/%: ##pull image
	docker pull $(OWNER)/$(notdir $@):${IMAGE_TAG}

docker.tag/%:
	docker tag $(OWNER)/$(notdir $@):${IMAGE_TAG} $(OWNER)/$(notdir $@):latest

docker.untag/%:
	aws ecr batch-delete-image --repository-name $(notdir $@) --image-ids imageTag=${IMAGE_TAG}

docker.push/%: ## push image
	docker push  $(OWNER)/$(notdir $@):${IMAGE_TAG}

docker.push-latest/%: ## push image
	docker push $(OWNER)/$(notdir $@):$latest

docker.clean: docker.rm-deps-all docker.cont-clean-all docker.img-rm-all ## clean environment

docker.login: ## login
	aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
