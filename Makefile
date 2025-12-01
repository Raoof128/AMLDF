.PHONY: install test lint format clean run

install:
	pip install -e .[dev]

test:
	python3 -m pytest

test-cov:
	python3 -m pytest --cov=backend --cov-report=term-missing --cov-report=html

lint:
	flake8 backend tests

typecheck:
	mypy backend --no-site-packages

format:
	black backend tests
	isort backend tests

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +

run:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
