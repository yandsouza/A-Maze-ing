PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean

install:
	$(PYTHON) -m pip install build

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

lint:
	flake8 --exclude=venv .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

build:
	$(PYTHON) -m build --wheel --outdir .

fix:
	pip config set global.index-url https://pypi.org/simple/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "maze.txt" -delete
	find . -type f -name "*.pyc" -delete
