# Makefile for drama_reverse_engine. Bind 127.0.0.1 only. pip-only (no `uv`).

PY  := python
PIP := pip
NPM := npm

.PHONY: install install-backend install-frontend run run-prod run-backend run-frontend build-frontend test test-backend test-frontend e2e boot-smoke probe clean

install: install-backend install-frontend

install-backend:
	$(PIP) install -r requirements.txt

install-frontend:
	cd apps/ui && $(NPM) install

run: run-backend

run-prod: build-frontend
	$(PY) -m apps.api.main --serve-static

run-backend:
	$(PY) -m apps.api.main

run-frontend:
	cd apps/ui && $(NPM) run dev

build-frontend:
	cd apps/ui && $(NPM) run build

run-worker:
	$(PY) -m apps.worker.main

probe:
	$(PY) -m apps.probe_cli.main $(ARGS)

test: test-backend

test-backend:
	$(PY) -m pytest tests -q

boot-smoke:
	$(PY) -m pytest tests/api/test_boot_smoke.py -q

e2e:
	cd apps/ui && npx playwright test
