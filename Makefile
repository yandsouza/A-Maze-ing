PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

.PHONY: install run debug clean

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

lint:
	flake8 .
	mypy --strict .

fix:
	pip config set global.index-url https://pypi.org/simple/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
