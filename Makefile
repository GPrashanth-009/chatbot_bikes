# Makefile for Bike Chatbot

.PHONY: help install install-dev test test-cov lint format clean run run-cli docker-build docker-run

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run all linting tools"
	@echo "  format       - Format code with Black and isort"
	@echo "  clean        - Clean up cache and temporary files"
	@echo "  run          - Run Streamlit web app"
	@echo "  run-cli      - Run CLI version"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run with Docker Compose"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Linting and formatting
lint:
	ruff check .
	black --check .
	isort --check-only .
	mypy .

format:
	black .
	isort .

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Running applications
run:
	streamlit run streamlit_app.py --server.port 3000

run-cli:
	python main.py

# Docker
docker-build:
	docker build -t bike-chatbot .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

# Development workflow
dev-setup: install-dev
	pre-commit install

pre-commit:
	pre-commit run --all-files

# Release tasks
release-check:
	@echo "Running release checks..."
	pytest tests/ --cov=. --cov-fail-under=80
	ruff check .
	black --check .
	isort --check-only .
	mypy .
	@echo "All checks passed!"

# Documentation
docs-serve:
	@echo "Starting documentation server..."
	@echo "Visit http://localhost:8000"
	python -m http.server 8000

# Environment setup
env-setup:
	@echo "Setting up development environment..."
	python -m venv .venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  source .venv/bin/activate  # Linux/Mac"
	@echo "  .\.venv\Scripts\Activate.ps1  # Windows"
	@echo "Then run: make install-dev"

# Quick start
quick-start: env-setup
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Setup complete! Run 'make run' to start the app."
