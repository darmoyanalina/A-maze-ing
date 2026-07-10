PYTHON      := python
ENTRY       := ./a_maze_ing.py
CONFIGS     := ./config.txt

.PHONY: install run debug clean lint lint-strict all re

all: run

install:
	poetry install
	poetry run pip install mazegen-0.1.0.tar.gz

run: install
	poetry run $(PYTHON) $(ENTRY) $(CONFIGS)

debug: install
	poetry run $(PYTHON) -m pdb $(ENTRY) $(CONFIGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache dist

lint:
	-poetry run flake8 .
	-poetry run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	-poetry run flake8 .
	-poetry run mypy . --strict

re: clean
	$(MAKE) run