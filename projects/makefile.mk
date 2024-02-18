## PROJECTS TARGETS

# Build start and test commands
ifeq ($(WITHOUT_DOCKER),true)
	BASE_CMD = cd ./projects/$(notdir $@)/$(COMPONENT)/ && python3 -m src
	ifeq ($(COMPONENT),ingest)
		START_CMD = $(BASE_CMD).$(COMPONENT)
	else ifeq ($(COMPONENT),register)
		START_CMD = $(BASE_CMD).$(COMPONENT)_features
	else ifneq (,$(filter $(COMPONENT), compile train)) # OR condition
		START_CMD = $(BASE_CMD).$(COMPONENT)_model
	else ifeq ($(COMPONENT),serve)
		START_CMD = $(BASE_CMD).$(COMPONENT).__main__
	endif
	UNIT_TEST_CMD = cd ./projects/$(notdir $@)/$(COMPONENT)/ && python3 -m pytest tests/unit -ra -vv --capture=no
else
	START_CMD = docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) up $(COMPONENT) --exit-code-from $(COMPONENT) --force-recreate --attach-dependencies
	UNIT_TEST_CMD = docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile unit up $(COMPONENT)-unit --exit-code-from $(COMPONENT)-unit --force-recreate --attach-dependencies
endif

projects.build/%: projects.set ## Build app
	@echo "::group::Build $(notdir projects/$@)-$(COMPONENT) (system architecture)"
	docker compose -f ./projects/$(notdir projects/$@)/docker-compose.$(ENVIRONMENT).yaml build $(COMPONENT) $(DOCKER_FLAGS)
	@echo "::endgroup::"

projects.install/%:
	poetry install --directory=projects/$(notdir $@)/$(COMPONENT)

projects.deploy/%: ## Deploy project component docker image to ECR.
	docker compose -f ./projects/$(notdir projects/$@)/docker-compose.$(ENVIRONMENT).yaml push $(COMPONENT)

projects.start/%: # Run main task of component in container
	$(START_CMD)

projects.debug/%:
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile debug up $(COMPONENT)-debug --exit-code-from $(COMPONENT)-debug --force-recreate --attach-dependencies

projects.run/%: # Run auxiliary task of component in container
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) up $(COMPONENT)-$(TASK) --exit-code-from $(COMPONENT)-$(TASK) --attach-dependencies

projects.stop/%: # Stop development container of component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.test/%: projects.unit/% projects.integration/% ## Run all tests for project component
	echo "Running all tests."

projects.unit/%: projects.set ## Run unit tests for project component
	$(UNIT_TEST_CMD)

projects.integration/%: ## Run integration tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile integration up $(COMPONENT)-integration --exit-code-from $(COMPONENT)-integration --force-recreate --attach-dependencies

projects.functional/%: ## Run functional tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile functional up $(COMPONENT)-functional --exit-code-from $(COMPONENT)-functional --force-recreate --attach-dependencies

	# ensure dependency service(s) shuts down
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.load/%: ## Run load tests for project component
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile load up $(COMPONENT)-load --exit-code-from $(COMPONENT)-load --force-recreate

	# ensure dependency service(s) shuts down
	docker compose -f projects/$(notdir $@)/docker-compose.$(ENVIRONMENT).yaml --profile $(COMPONENT) down

projects.lock/%:
	poetry lock --directory=projects/$(notdir $@)/$(COMPONENT)

projects.env/%:
	poetry env info --directory=projects/$(notdir $@)/$(COMPONENT)

projects.activate/%:
	poetry shell --directory=projects/$(notdir $@)/$(COMPONENT)

projects.set:
	export IMAGE_TAG=$(IMAGE_TAG)
	export TARGET_BUILD_STAGE=$(TARGET_BUILD_STAGE)
	export AWS_ACCOUNT_ID=$(AWS_ACCOUNT_ID)
