# jimeng_web_bridge — bind 127.0.0.1 only. pip-only (no `uv`).

PY   := python
NPM  := npm
VENV := .venv
VENV_PY = $$(if [ -f "$(VENV)/Scripts/python.exe" ]; then echo "$(VENV)/Scripts/python.exe"; else echo "$(VENV)/bin/python"; fi)

.PHONY: venv init install ui-build run test test-perf test-soak canary

venv:
	@[ -f "$(VENV)/Scripts/python.exe" ] || [ -f "$(VENV)/bin/python" ] || ( $(PY) -m venv "$(VENV)" && "$(VENV_PY)" -m pip install --upgrade pip && "$(VENV_PY)" -m pip install -r requirements.txt )

install: venv
	"$(VENV_PY)" -m pip install -r requirements.txt
	"$(VENV_PY)" -m playwright install chromium
	cd apps/ui && $(NPM) install

init: venv
	"$(VENV_PY)" -m apps.api.init_cli

ui-build:
	cd apps/ui && $(NPM) run build

run: venv
	"$(VENV_PY)" -m apps.api.main

test: venv
	"$(VENV_PY)" -m pytest tests -m "not perf and not soak"

test-perf: venv
	"$(VENV_PY)" -m pytest tests -m perf

test-soak: venv
	"$(VENV_PY)" -m pytest tests -m soak

canary: venv
	"$(VENV_PY)" -m apps.api.canary_cli
