.PHONY: install run clean lint format help

# Default target
.DEFAULT_GOAL := help

install: ## Install dependencies using uv
	uv sync

run: ## Run the application
	uv run main.py

clean: ## Remove temporary files and caches
	rm -rf .venv
	rm -rf .ruff_cache
	rm -rf __pycache__
	rm -rf linkedin_helper/__pycache__
	rm -rf linkedin_helper.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint: ## Run linting with ruff
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
