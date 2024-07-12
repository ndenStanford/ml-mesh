## APPS TARGETS

apps.build/%: apps.set ## Build app
	@echo "::group::Build $(OWNER)/$(notdir apps/$@)-$(COMPONENT) (system architecture)"
	docker compose -f ./apps/$(notdir apps/$@)/docker-compose.$(ENVIRONMENT).yaml build $(COMPONENT) $(DOCKER_FLAGS)
	@echo "::endgroup::"

apps.install/%:
	poetry install --directory=apps/$(notdir $@)/$(COMPONENT)

apps.deploy/%: ## Deploy project component docker image to ECR.
	docker compose -f ./apps/$(notdir apps/$@)/docker-compose.$(ENVIRONMENT).yaml push $(COMPONENT)

apps.start/%: # Start development container of component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) up --force-recreate

apps.debug/%: # Start debugger container of component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile debug up $(COMPONENT)-debug --force-recreate --attach-dependencies

apps.stop/%: # Start development container of component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

apps.test/%: apps.unit/% apps.integration/% ## Run all tests for project component
	echo "Running all tests."

apps.unit/%: apps.set ## Run unit tests for project component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile unit up $(COMPONENT)-unit --exit-code-from $(COMPONENT)-unit --force-recreate

apps.functional/%: ## Run functional tests for project component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile functional up $(COMPONENT)-functional --exit-code-from $(COMPONENT)-functional --force-recreate --attach-dependencies

apps.integration/%: ## Run integration tests for project component
	docker compose -f apps/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile integration up $(COMPONENT)-integration --exit-code-from $(COMPONENT)-integration --force-recreate

apps.lock/%:
	poetry lock --directory=apps/$(notdir $@)/$(COMPONENT)

apps.set:
	export OWNER=$(OWNER)
	export DEPLOYMENT=$(DEPLOYMENT)
	export IMAGE_TAG=$(IMAGE_TAG)
	export TARGET_BUILD_STAGE=$(TARGET_BUILD_STAGE)
	export AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID)
