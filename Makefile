PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: validate
validate:
	$(PYTHON) .scripts/validate.py
