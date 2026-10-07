PYTHON ?= python

dev:
	$(PYTHON) -m apps.desktop.main
test:
	$(PYTHON) -m pytest -q
lint:
	$(PYTHON) -m compileall -q apps libs
build: lint
