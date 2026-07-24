PYTHON = python3
SCRIPT = main.py
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
	flake8 main.py
	mypy --warn-return-any \
	     --warn-unused-ignores \
	     --ignore-missing-imports \
	     --disallow-untyped-defs \
	     --check-untyped-defs main.py

lint-strict:
	flake8 main.py
	mypy --strict main.py

.PHONY: install run debug clean lint lint-strict