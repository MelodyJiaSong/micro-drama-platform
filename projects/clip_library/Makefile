PYTHON ?= .venv/Scripts/python.exe

dev:
	$(PYTHON) -m apps.cli.main --help
test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m compileall -q apps libs
build: lint
