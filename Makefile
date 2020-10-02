default: install

# Show summary of make commands.
help:
	@echo 'Print lines that are not indented (targets and comments) or empty, plus any indented echo lines.'
	@egrep '(^\S)|(^$$)|\s+@echo' Makefile


# Install core dependencies.
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Install dev dependencies.
install-dev:
	pip install -r requirements-dev.txt


# Apply Black formatting fixes to Python files.
format:
	black .
format-check:
	black . --diff --check

check-types:
	mypy ghgql
