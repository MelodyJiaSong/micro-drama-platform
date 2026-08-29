PY := ../../.venv/Scripts/python

.PHONY: test rubric-validate estimate run report

test:
	$(PY) -m pytest tests -q

rubric-validate:
	$(PY) -m apps.cli.main rubric validate

estimate:
	$(PY) -m apps.cli.main estimate --project $(PROJECT)

run:
	$(PY) -m apps.cli.main run --project $(PROJECT)

report:
	$(PY) -m apps.cli.main report --project $(PROJECT)
