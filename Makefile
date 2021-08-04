CONFIG_TEMPL = app.template.yml
CONFIG_LOCAL = app.local.yml


default: install install-dev

all: install install-dev fmt-check lint typecheck


h help:
	@grep '^[a-z]' Makefile


install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

upgrade:
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade

config:
	cd ghgql/etc && \
		cp $(CONFIG_TEMPL) $(CONFIG_LOCAL) && \
		open $(CONFIG_LOCAL)


fmt:
	black .
fmt-check:
	black . --diff --check

l lint:
	flake8 . --select=E9,F63,F7,F82 --show-source
	flake8 . --exit-zero

fix: format lint

t typecheck:
	mypy ghgql


demo:
	# Basic demo.
	cd ghgql && python -m demo.basic

	# Variables demo.
	cd ghgql && python -m demo.variables

	# Paginate demo.
	cd ghgql && python -m demo.paginate
