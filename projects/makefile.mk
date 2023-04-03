## PROJECTS TARGETS

projects.build/%: ## Build project
	@echo "::group::Build $(OWNER)/$(notdir projects/$@)-$(COMPONENT) (system architecture)"
	docker build $(DOCKER_BUILD_ARGS) . \
			-t $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG} \
			-f ./projects/$(notdir $@)/$(COMPONENT)/Dockerfile	\
			--build-arg OWNER="$(OWNER)" \
			--build-arg PROJECT=$(notdir $@) \
			--build-arg COMPONENT=$(COMPONENT) \
			--build-arg IMAGE_TAG="$(IMAGE_TAG)" \
			--platform=$(PLATFORM) \
			$(DOCKER_EXTRA_FLAGS) \
			--rm --force-rm
	@echo -n "built image size:"
	@docker images $(OWNER)/$(notdir $@)-$(COMPONENT):latest --format "{{.Size}}"
	@echo "::endgroup::"

projects.install/%:
	poetry install --directory=projects/$(notdir $@)/$(COMPONENT)

projects.deploy/%: ## Deploy project component docker image to ECR.
	docker push  $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG}

projects.tag/%:
	docker tag $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG} $(OWNER)/$(notdir $@)-$(COMPONENT):latest

projects.untag/%:
	aws ecr batch-delete-image --repository-name $(notdir $@)-$(COMPONENT) --image-ids imageTag="latest"

projects.start/%: # Start development container of component
	cd projects/$(notdir $@)/$(COMPONENT) && $(DOCKER_CMD) uvicorn src.app:app --host 0.0.0.0 --port $(PORT) --reload --log-level "debug"

projects.test/%: projects.unit/% projects.integration/% ## Run all tests for project component
	echo "Running all tests."

projects.unit/%: ## Run unit tests for project component
	cd projects/$(notdir $@)/$(COMPONENT) && $(DOCKER_CMD) pytest tests/unit -ra -vvv --tb=long --capture=no

projects.integration/%: ## Run integration tests for project component
	cd projects/$(notdir $@)/$(COMPONENT) && $(DOCKER_CMD) pytest tests/integration -ra -vvv --tb=long --capture=no

projects.lock/%:
	poetry lock --directory=projects/$(notdir $@)/$(COMPONENT)
