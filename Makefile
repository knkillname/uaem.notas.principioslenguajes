.PHONY: clean
NOTAS_IPYNB=$(wildcard notas/*.ipynb)
DIR_HTML=dist/html
NOTAS_HTML=$(patsubst notas/%.ipynb, $(DIR_HTML)/%.html, $(NOTAS_IPYNB))

default: venv format lint test coverage

venv: .venv/bin/activate
.venv/bin/activate: Pipfile
	pipenv install --dev
	pipenv run pip install -e .
	touch $@

html: $(NOTAS_HTML)
$(DIR_HTML)/%.html: notas/%.ipynb
	mkdir -p notas/html
	pipenv run jupyter nbconvert --to html --execute --output-dir $(DIR_HTML) $<

format: venv
	pipenv run isort .
	pipenv run black .

lint: venv
	pipenv run isort --check src notas tests
	pipenv run black --check src notas tests
	pipenv run pylint src notas tests
	pipenv run mypy src tests

test: venv
	pipenv run python -m unittest discover -s tests

coverage: venv
	pipenv run coverage run --source=src -m unittest discover -s tests
	pipenv run coverage report -m
	pipenv run coverage html

clean:
	git clean -Xdf