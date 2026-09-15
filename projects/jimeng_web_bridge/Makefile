# jimeng_web_bridge — bind 127.0.0.1 only. pip-only (no `uv`).

PY   := python
NPM  := npm
VENV := .venv
VENV_PY = $$(if [ -f "$(VENV)/Scripts/python.exe" ]; then echo "$(VENV)/Scripts/python.exe"; else echo "$(VENV)/bin/python"; fi)

.PHONY: venv init install ui-build ui-contract run test test-signoff test-perf test-soak canary probe probe-capture

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

# Rewrites apps/ui/test/fixtures/contract/*.json from the response DTOs; the UI build type-checks against them.
ui-contract: venv
	"$(VENV_PY)" -m tests.contract.ui_contract

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

test-signoff: venv
	JWB_REQUIRE_REAL_REPO=1 JWB_REQUIRE_FFPROBE=1 "$(VENV_PY)" -m pytest tests -m "not perf and not soak"

# Read-only probes of the real site in the service's own Chrome profile (scan the QR code when asked).
# They never click 生成/发布/删除/保存/确认 and never spend credits.
probe-capture: venv
	"$(VENV_PY)" tests/probe/site_probe_phase1.py

probe: venv
	"$(VENV_PY)" tests/probe/site_probe_phase2.py
