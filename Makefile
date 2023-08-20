export PIPENV_VENV_IN_PROJECT=1

".venv": Pipfile
	pipenv install --dev
