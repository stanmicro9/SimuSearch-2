# Makefile for Scientific Agents project

.PHONY: install setup test run clean lint format docker-build docker-run

# Installation and setup
install:
	pip install -r requirements.txt

setup: install
	cp .env.example .env
	@echo "Please edit .env file with your API keys"

dev-install: install
	pip install -e .
	pip install -r requirements-dev.txt

# Testing
test:
	pytest tests/ -v --cov=src

test-integration:
	pytest tests/test_integration.py -v -s

# Running the application
run:
	python -m src.main

interactive:
	python -m src.cli_interface

example:
	python -m src.main "How does temperature affect chemical reaction rates?"

# Code quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

check: lint test

# Docker operations
docker-build:
	docker build -t scientific-agents .

docker-run:
	docker-compose up

docker-clean:
	docker-compose down -v

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# Documentation
docs:
	@echo "Generating documentation..."
	python -c "from src.agents.core.theoretical_agent import TheoreticalAgent; help(TheoreticalAgent)"

# Project structure
structure:
	tree -I '__pycache__|*.pyc|venv|.git'

# Quick start
quickstart: setup
	@echo "🚀 Quick start complete!"
	@echo "1. Edit .env file with your GOOGLE_API_KEY"
	@echo "2. Run: make run"
	@echo "3. Enter your scientific question when prompted"