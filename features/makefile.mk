features.install:
	poetry --directory=features install --with dev

features.lock:
	poetry --directory=features lock

features.plan:
	python3 features/src/__main__.py features plan

features.apply:
	python3 features/src/__main__.py features apply

features.test:
	pytest features/tests --capture=no -ra -vvv --full-trace --tb=long
