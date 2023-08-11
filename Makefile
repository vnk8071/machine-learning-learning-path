#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

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
