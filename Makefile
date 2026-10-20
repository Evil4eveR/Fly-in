PYTHON = python3
FILE ?= maps/easy/02_simple_fork.txt

all: run

install:
	@echo "No external dependencies to install."

run:
	$(PYTHON) main.py $(FILE)

debug:
	$(PYTHON) -m pdb main.py $(FILE)

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict