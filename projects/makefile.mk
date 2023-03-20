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
			--rm --force-rm --no-cache
	@echo -n "built image size:"
	@docker images $(OWNER)/$(notdir $@)-$(COMPONENT):latest --format "{{.Size}}"
	@echo "::endgroup::"

projects.test/%: projects.unit/% projects.integration/% ## Run all tests for project component
	echo "Running all tests."

projects.unit/%: ## Run unit tests for project component
	python -m pytest projects/$(notdir $@)/$(COMPONENT)/tests/unit -ra -vvv --full-trace --tb=long

projects.integration/%: ## Run integration tests for project component
	python -m pytest projects/$(notdir $@)/$(COMPONENT)/tests/integration -ra -vvv --full-trace --tb=long

projects.deploy/%: ## Deploy project component docker image to ECR.
	docker push  $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG}

projects.start/%: # Start development container of component
	docker-compose -f projects/$(notdir $@)/docker-compose.dev.yaml --profile $(COMPONENT) up

projects.stop/%: # Stop development container of component
	docker-compose -f projects/$(notdir $@)/docker-compose.dev.yaml --profile $(COMPONENT) down

projects.install/%:
	poetry install --directory=projects/$(notdir $@)/$(COMPONENT)

projects.tag/%:
	docker tag $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG} $(OWNER)/$(notdir $@)-$(COMPONENT):latest

projects.untag/%:
	aws ecr batch-delete-image --repository-name $(notdir $@)-$(COMPONENT) --image-ids imageTag="latest"
