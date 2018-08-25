# Makefile for Python Wechaty
# Author: Huan LI <zixia@zixia.net> git.io/zixia

SOURCE_GLOB=$(wildcard bin/*.py src/*.py src/**/*.py tests/*.py)

.PHONY: all
all : clean lint

.PHONY: clean
clean:
	rm -fr dist/*

.PHONY: lint
lint: pylint pycodestyle flake8 mypy

.PHONY: pylint
pylint:
	pylint $(SOURCE_GLOB)

.PHONY: pycodestyle
pycodestyle:
	pycodestyle --statistics --count $(SOURCE_GLOB)

.PHONY: flake8
flake8:
	flake8 $(SOURCE_GLOB)

.PHONY: mypy
mypy:
	MYPYPATH=stubs/ mypy \
		--python-version=3 \
		$(SOURCE_GLOB)

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: pytest
pytest:
	PYTHONPATH=src/ pytest src/ tests/

.PHONY: test
test: check-version pytest

.PHONY: check-version
check-version:
	./scripts/check_version.py

code:
	PYTHONPATH=src/ code .

.PHONY: run
run:
	PYTHONPATH=src/ python3 bin/run.py

.PHONY: dist
dist:
	python3 setup.py sdist bdist_wheel

.PHONY: publish
publish:
	PATH=~/.local/bin:${PATH} twine upload dist/*
