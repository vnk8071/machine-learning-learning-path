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
	docker build -t flask-app .
	docker run -p 5000:5000 flask-app

docker-stop:
	docker stop flask-app

.PHONY: docker-compose-up
docker-compose-up:
	docker compose up --build

.PHONY: docker-compose-down
docker-compose-down:
	docker compose down

#* CI
.PHONY: ci
ci: pre-commit lint test
