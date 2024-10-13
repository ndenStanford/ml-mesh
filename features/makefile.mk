features.install:
	poetry --directory=features install --with dev

features.lock:
	poetry --directory=features lock

features.plan:
	python3 features/onclusiveml/features/__main__.py features plan

features.apply:
	python3 features/onclusiveml/features/__main__.py features apply

features.test:
	pytest features/onclusiveml/tests --capture=no -ra -vvv --full-trace --tb=long
