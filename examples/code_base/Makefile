#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Installation
.PHONY: install
install:
	pip install -r requirements.txt

#* Application
.PHONY: run
run:
	python app.py

#* Linting
.PHONY: lint
lint:
	flake8 --max-line-length=120 --exclude=venv --verbose

#* Testing
.PHONY: test
test:
	pytest --verbose tests

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

#* Docker
.PHONY: docker-build-run
docker-build-run:
	docker build -t web-app .
	docker run -p 5000:5000 web-app

docker-stop:
	docker stop web-app

.PHONY: docker-compose-up
docker-compose-up:
	docker compose up --build

.PHONY: docker-compose-down
docker-compose-down:
	docker compose down

#* Format
.PHONY: format
format:
	autopep8 --verbose --in-place --aggressive --aggressive --max-line-length=120 **/*.py

#* CI
.PHONY: ci
ci: pre-commit lint test
