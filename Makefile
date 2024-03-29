CONFIG_TEMPL = app.template.yml
CONFIG_LOCAL = app.local.yml


default: install install-dev

all: install install-dev checks


h help:
	@grep '^[a-z]' Makefile


install:
	pip install pip --upgrade
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	mypy --install-types --non-interactive

upgrade:
	pip install pip --upgrade
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade

config:
	cd ghgql/etc && \
		cp $(CONFIG_TEMPL) $(CONFIG_LOCAL) && \
		open $(CONFIG_LOCAL)


fmt-fix:
	black .
	isort .
fmt-check:
	black . --diff --check
	isort . --check

l lint:
	flake8 . --select=E9,F63,F7,F82 --show-source
	flake8 . --exit-zero

t typecheck:
	mypy ghgql

checks: fmt-check lint typecheck


demo:
	# Basic demo.
	cd ghgql && python -m demo.basic

	# Variables demo.
	cd ghgql && python -m demo.variables

	# Paginate demo.
	cd ghgql && python -m demo.paginate

# Reports with hardcoded values, useful for the codeowner to test changes.

report-commit:
	cd ghgql && ./repo_commits.py MichaelCurrin github-reporting-py

report-counts:
	cd ghgql && ./repos_and_commit_counts.py owner MichaelCurrin start 2021-01-01

report: report-commit report-counts
