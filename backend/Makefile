.DEFAULT_GOAL := help
PROJECT_NAME := backend-chron-track
PYTHON_VERSION := 3.13

###############################
# Tests
###############################

test: ## Run the tests
	uv run pytest

coverage: ## Run the tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

###############################
# Linter
###############################

lint: ## Run the linter
	@uvx ruff check --select=I --fix .
	@uvx ruff check --fix .

pretty: ## Format the code
	@uvx ruff format .

pre-commit: ## Run the pre-commit hooks
	@uvx pre-commit run --all-files

type-check: ## Run the type checker
	@uv run mypy src

###############################
# Help
###############################

help: ## Show this help
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' 