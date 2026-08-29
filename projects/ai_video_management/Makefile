# Makefile for ai_video_management (post follow-up 039: apps/+libs/ layout).
# Bind 127.0.0.1 only. pip-only (no `uv`).

PY  := python
PIP := pip
NPM := npm
VENV := .venv

# Interpreter inside the venv. Resolved by the shell when a recipe runs, not
# by make at parse time, so it is still correct when the venv was created
# earlier in the same run. Windows venvs use Scripts/, POSIX ones use bin/.
VENV_PY = $$(if [ -f "$(VENV)/Scripts/python.exe" ]; then echo "$(VENV)/Scripts/python.exe"; else echo "$(VENV)/bin/python"; fi)

.PHONY: venv create-venv install install-backend install-frontend run run-prod run-backend run-frontend build-frontend test test-backend test-frontend e2e boot-smoke clean

install: install-backend install-frontend

install-backend:
	$(PIP) install -r requirements.txt

install-frontend:
	cd apps/ui && $(NPM) install

run: run-backend

run-prod: build-frontend run-backend

# Use $(VENV); create and provision it first if it is missing.
venv:
	@[ -f "$(VENV)/Scripts/python.exe" ] || [ -f "$(VENV)/bin/python" ] || $(MAKE) create-venv

create-venv:
	@echo ">> No $(VENV) found - creating it"
	$(PY) -m venv "$(VENV)"
	@echo ">> Installing requirements into $(VENV)"
	"$(VENV_PY)" -m pip install --upgrade pip
	"$(VENV_PY)" -m pip install -r requirements.txt

run-backend: venv
	"$(VENV_PY)" -m apps.api.main

run-frontend:
	cd apps/ui && $(NPM) run dev

build-frontend:
	cd apps/ui && $(NPM) run build

test: test-backend test-frontend

test-backend:
	$(PY) -m pytest tests/ -v

test-frontend:
	cd apps/ui && $(NPM) test

e2e:
	cd apps/ui && $(NPM) run test:e2e

boot-smoke:
	$(PY) -m pytest tests/test_boot_smoke.py -v

clean:
	rm -rf apps/ui/node_modules apps/ui/dist apps/ui/.vite apps/api/static/assets apps/api/static/index.html
	find apps libs tests -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type d -name .pytest_cache -exec rm -rf {} + || true
