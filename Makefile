default: install install-dev

all: install install-dev format-check lint typecheck


h help:
	@grep '^[a-z]' Makefile


install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt


format:
	black .
format-check:
	black . --diff --check

l lint:
	flake8 . --select=E9,F63,F7,F82 --show-source
	flake8 . --exit-zero

fix: format lint

t typecheck:
	mypy ghgql
