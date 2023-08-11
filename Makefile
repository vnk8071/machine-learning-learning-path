#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | $(PYTHON) - --uninstall

#* Installation
.PHONY: install
install:
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install

#* Pre-commit
.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files

#* Lint
.PHONY: codestyle
codestyle:
	poetry run autopep8 --in-place --aggressive --aggressive .

#* CI
.PHONY: ci
ci:
	poetry run pylint --rcfile=.pylintrc --output-format=colorized --reports=n --fail-under=9.5 --jobs=0 --score=no src


#* Tests
.PHONY: tests
tests:
	poetry run pytest churn_script_logging_and_tests.py
