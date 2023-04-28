# LIBS targets

libs.install/%: ## Installs library and dependencies locally
	poetry install --directory=libs/$(notdir $@)

libs.unit/%: ## Run unit tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/unit -ra -vvv --full-trace --tb=long --capture=no

libs.integration/%: ## Run integration tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/integration -ra -vvv --full-trace --tb=long --capture=no

libs.functional/%: ## Run functional tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/functional -ra -vvv --full-trace --tb=long --capture=no

libs.test/%: libs.unit/% libs.integration/% libs.functional/% ## Run the full (unit, integration & functional) test suite
	@echo "Run full test suite for library $(notdir $@)..."

libs.unit-all: $(foreach I, $(ALL_LIBS), libs.unit/$(I)) # run unit test for all libraries

libs.integration-all: $(foreach I, $(ALL_LIBS), libs.integration/$(I)) # run integration test for all libraries

libs.functional-all: $(foreach I, $(ALL_LIBS), libs.functional/$(I)) # run functional test for all libraries

libs.test-all: $(foreach I, $(ALL_LIBS), libs.test/$(I)) # run full test suite for all libraries

libs.install-all: $(foreach I, $(ALL_LIBS), libs.install/$(I)) # install library dependencies
