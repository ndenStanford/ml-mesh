# LIBS targets

libs.install/%:
	poetry install --directory=libs/$(notdir $@)

libs.unit/%: ## Run unit tests for lib
	python -m pytest libs/$(notdir $@)/onclusiveml/tests/unit -ra -vvv --full-trace --tb=long

libs.test-all: $(foreach I, $(ALL_LIBS), libs.unit/$(I)) # run test on all libraries

libs.install-all: $(foreach I, $(ALL_LIBS), libs.install/$(I)) # install library dependencies
