export PIPENV_VENV_IN_PROJECT=1

.PHONY: clean

default: ".venv"
".venv": Pipfile
	pipenv install --dev

format: ".venv"
	pipenv run isort .
	pipenv run black .

lint: ".venv"
	pipenv run isort --check src notas
	pipenv run black --check src notas
	pipenv run pylint src notas

clean:
	git clean -Xdf