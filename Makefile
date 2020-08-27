SHELL = /bin/bash

PYTHON = python3

VIRTUALENV = $(PYTHON) -m venv
VENV_DIR = .venv
VENV_PYTHON = .venv/bin/python
VENV_PIP = .venv/bin/pip
VENV_PYTEST = .venv/bin/pytest


.PHONY: default
default: all


$(VENV_DIR):
	$(VIRTUALENV) $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip setuptools wheel
	$(VENV_PIP) install -r requirements-dev.txt
	$(VENV_PIP) install -e .


.PHONY: venv
venv: $(VENV_DIR)


.PHONY: clean
clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf htmlcov
	rm -f .coverage


.PHONY: realclean
realclean:
	rm -rf $(VENV_DIR)
	rm -rf *.egg-info


.PHONY: build
build: venv clean


.PHONY: test
test: build
	$(VENV_PYTEST) tests/ --tb=native --cov=posed --cov-report=term


.PHONY: dist
dist: test
	$(VENV_PYTHON) setup.py sdist bdist_wheel


.PHONY: all
all: dist
