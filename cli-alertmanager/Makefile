# Webhooks Alertmanager Automation Makefile

# Variables
VENV ?= venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
FLAKE8 := $(VENV)/bin/flake8
BLACK := $(VENV)/bin/black

PKG := webhook_glpi
IMAGE ?= webhooks-alertmanager
GIT_SHA := $(shell git rev-parse --short HEAD)
TAG ?= $(shell git describe --tags --always --dirty)
PORT ?= 5000

.PHONY: help install install-dev test test-cov lint format clean build run docker-build docker-run docker-compose-up docker-compose-down tag push-tag qa venv

# Default target
help:
	@echo "Available commands:"
	@echo "  install        Install production dependencies"
	@echo "  install-dev    Install development dependencies"
	@echo "  test           Run tests"
	@echo "  test-cov       Run tests with coverage"
	@echo "  format         Format code with black"
	@echo "  lint           Run flake8 linting (warnings only)"
	@echo "  qa             Run quality assurance (format + lint + tests)"
	@echo "  clean          Clean build artifacts"
	@echo "  build          Build the package"
	@echo "  run            Run the Flask application"
	@echo "  docker-build   Build Docker image"
	@echo "  docker-run     Run Docker container"
	@echo "  docker-compose-up   Start with docker-compose"
	@echo "  docker-compose-down Stop docker-compose services"
	@echo "  tag            Create and push git tag"
	@echo "  push-tag       Push tags to origin"

# Virtual environment target
venv: ## Create/refresh virtualenv
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install -U pip setuptools wheel

# Installation targets
install: venv ## Install production dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: venv ## Install dev deps (pytest, coverage, flake8, black)
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov flake8 black
	$(PIP) install -e .
	@echo "Virtual environment created at $(VENV)"
	@echo "To activate: source $(VENV)/bin/activate"

# Testing targets
test: ## Run tests
	@if [ ! -d "$(VENV)" ]; then echo "Run 'make install-dev' first"; exit 1; fi
	$(PYTEST) tests/ -v

test-cov: ## Run tests with coverage
	@if [ ! -d "$(VENV)" ]; then echo "Run 'make install-dev' first"; exit 1; fi
	$(PYTEST) tests/ --cov=$(PKG) --cov-report=html --cov-report=term-missing -v

# Code quality targets
format: ## Format code with black
	@if [ ! -d "$(VENV)" ]; then echo "Run 'make install-dev' first"; exit 1; fi
	$(BLACK) $(PKG)/ app.py

lint: ## Run flake8 linting (warnings only, doesn't fail)
	@if [ ! -d "$(VENV)" ]; then echo "Run 'make install-dev' first"; exit 1; fi
	-$(FLAKE8) $(PKG)/ app.py --max-line-length=120 --extend-ignore=E203,W503
	@echo "Lint warnings shown above (if any) - this doesn't block the build"

qa: format lint test ## Run quality assurance (format + lint + tests)
	@echo "Quality assurance checks completed successfully!"

# Build and clean targets
clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -delete
	find . -name "*.pyc" -delete

build: clean ## Build the package
	$(PYTHON) setup.py sdist bdist_wheel

# Application targets
run: ## Run the Flask application
	$(PYTHON) app.py

# Docker targets
docker-build: ## Build Docker image
	docker build -t $(IMAGE) .

docker-run: ## Run Docker container
	docker run -p $(PORT):$(PORT) $(IMAGE)

docker-compose-up: ## Start with docker-compose
	docker-compose up --build

docker-compose-down: ## Stop docker-compose services
	docker-compose down

# Git targets
tag: ## Create and push git tag
	git tag "1.0.0-$(GIT_SHA)"
	git push origin --tag

push-tag: ## Push tags to origin
	git push origin --tags

# Webhook testing payload
test-webhook: ## Test webhook with working payload
	curl -X POST http://localhost:5000/glpi \
		-H "Content-Type: application/json" \
		-d @request_payload.json
