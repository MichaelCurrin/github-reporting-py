default: install

help:
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

check-types:
	mypy ghgql
