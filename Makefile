export PIPENV_VENV_IN_PROJECT=1

.PHONY: clean

default: ".venv" format lint test coverage

".venv": Pipfile
	pipenv install --dev
	pipenv run pip install -e .

format: ".venv"
	pipenv run isort .
	pipenv run black .

lint: ".venv"
	pipenv run isort --check src notas
	pipenv run black --check src notas
	pipenv run pylint src notas

test: ".venv"
	pipenv run python -m unittest discover -s tests

coverage: ".venv"
	pipenv run coverage run --source=src -m unittest discover -s tests
	pipenv run coverage report -m
	pipenv run coverage html

clean:
	git clean -Xdf