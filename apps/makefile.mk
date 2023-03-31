## APPS TARGETS

apps.build/%: apps.set ## Build app
	@echo "::group::Build $(OWNER)/$(notdir apps/$@)-$(COMPONENT) (system architecture)"
	docker-compose -f ./apps/$(notdir apps/$@)/docker-compose.dev.yaml build --no-cache
	@echo "::endgroup::"

apps.install/%:
	poetry install --directory=apps/$(notdir $@)/$(COMPONENT)

apps.deploy/%: ## Deploy project component docker image to ECR.
	docker push  $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG}

apps.tag/%:
	docker tag $(OWNER)/$(notdir $@)-$(COMPONENT):${IMAGE_TAG} $(OWNER)/$(notdir $@)-$(COMPONENT):latest

apps.untag/%:
	aws ecr batch-delete-image --repository-name $(notdir $@)-$(COMPONENT) --image-ids imageTag="latest"

apps.start/%: # Start development container of component
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml up

apps.stop/%: # Start development container of component
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml down

apps.test/%: apps.unit/% apps.integration/% ## Run all tests for project component
	echo "Running all tests."

apps.unit/%: apps.set ## Run unit tests for project component
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml up -d
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml exec prompt pytest tests/unit -ra -vvv --tb=long --capture=no

apps.integration/%: ## Run integration tests for project component
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml up -d
	docker compose -f apps/$(notdir $@)/docker-compose.dev.yaml exec prompt pytest tests/unit -ra -vvv --tb=long --capture=no

apps.lock/%:
	poetry lock --directory=apps/$(notdir $@)/$(COMPONENT)

apps.set:
	export OWNER=$(OWNER)
	export IMAGE_TAG=$(IMAGE_TAG)