PYTHON ?= $(abspath ../../.venv/Scripts/python.exe)

dev:
	cd ../.. && $(PYTHON) -m projects.suno_browser_service.apps.api.main
test:
	$(PYTHON) -m pytest
lint:
	$(PYTHON) -m compileall -q apps libs
ui:
	cd apps/ui && npm ci && npm run build
build: ui lint test
login:
	cd ../.. && $(PYTHON) -m projects.suno_browser_service.apps.login.main
