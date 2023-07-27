## PROJECTS TARGETS

projects.build/%: projects.set ## Build app
	@echo "::group::Build $(notdir projects/$@)-$(COMPONENT) (system architecture)"
	docker compose -f ./projects/$(notdir projects/$@)/docker-compose.$(ENVIRONMENT).yaml build $(COMPONENT) --no-cache
	@echo "::endgroup::"

projects.install/%:
	poetry install --directory=projects/$(notdir $@)/$(COMPONENT)

projects.deploy/%: ## Deploy project component docker image to ECR.
	docker compose -f ./projects/$(notdir projects/$@)/docker-compose.$(ENVIRONMENT).yaml push $(COMPONENT)

projects.start/%: # Start development container of component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) up $(COMPONENT) --force-recreate

projects.stop/%: # Start development container of component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.test/%: projects.unit/% projects.integration/% ## Run all tests for project component
	echo "Running all tests."

projects.unit/%: projects.set ## Run unit tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile unit up $(COMPONENT)-unit --exit-code-from $(COMPONENT)-unit --force-recreate

projects.integration/%: ## Run integration tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile integration up $(COMPONENT)-integration

projects.functional/%: ## Run functional tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile functional up $(COMPONENT)-functional --exit-code-from $(COMPONENT)-functional --force-recreate

	# ensure dependency service(s) shuts down
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.load/%: ## Run load tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile load up $(COMPONENT)-load --exit-code-from $(COMPONENT)-load --force-recreate

	# ensure dependency service(s) shuts down
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.compile/%: ## Run model compilation pipeline component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile pipeline up compile-$(PIPELINE_COMPONENT) --exit-code-from compile-$(PIPELINE_COMPONENT)

projects.lock/%:
	poetry lock --directory=projects/$(notdir $@)/$(COMPONENT)

projects.set:
	export IMAGE_TAG=$(IMAGE_TAG)
	export TARGET_BUILD_STAGE=$(TARGET_BUILD_STAGE)
	export AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID)
