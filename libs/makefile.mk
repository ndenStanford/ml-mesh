# LIBS targets

libs.install/%:
	poetry install --directory=libs/$(notdir $@)

libs.unit/%: ## Run unit tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/unit -ra -vvv --full-trace --tb=long

libs.integration/%: ## Run unit tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/integration -ra -vvv --full-trace --tb=long

libs.test-all: $(foreach I, $(ALL_LIBS), libs.unit/$(I)) # run unit tests on all libraries

libs.test-all-integration: $(foreach I, $(ALL_LIBS), libs.integration/$(I)) # run integration tests on all libraries

libs.install-all: $(foreach I, $(ALL_LIBS), libs.install/$(I)) # install library dependencies
