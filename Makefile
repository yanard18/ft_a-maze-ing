PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt


install:
	$(PYTHON) -m pip install flake8 mypy build

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf __pycache__ */__pycache__
	rm -rf .mypy_cache
	rm -rf build dist *.egg-info

build:
	$(PYTHON) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .

lint:
	flake8 .
	mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean build lint lint-strict
