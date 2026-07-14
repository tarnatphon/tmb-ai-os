PYTHON ?= python3.13
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: bootstrap install install-dev run test lint format format-check compile check clean

bootstrap:
	./scripts/bootstrap.sh

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install ruff pytest

run:
	$(VENV)/bin/uvicorn app.main:app --reload

test:
	$(PY) -m pytest -q

lint:
	$(VENV)/bin/ruff check app tests

format:
	$(VENV)/bin/ruff format app tests
	$(VENV)/bin/ruff check --fix app tests

format-check:
	$(VENV)/bin/ruff format --check app tests

compile:
	$(PY) -m compileall -q app tests

check: compile format-check lint test

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
