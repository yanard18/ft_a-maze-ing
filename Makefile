PYTHON = python3
SCRIPT = a_maze_ing.py
FILES = test.py mazegen.py a_maze_ing.py
CONFIG = config.txt


install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache

lint:
	flake8 $(FILES)
	mypy --warn-return-any \
	     --warn-unused-ignores \
	     --ignore-missing-imports \
	     --disallow-untyped-defs \
	     --check-untyped-defs $(FILES)

lint-strict:
	flake8 $(FILES)
	mypy --strict $(FILES)

.PHONY: install run debug clean lint lint-strict