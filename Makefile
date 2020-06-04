# Makefile for Python Wechaty
#
# 	GitHb: https://github.com/wechaty/python-wechaty
# 	Author: Huan LI <zixia@zixia.net> https://github.com/huan
#

SOURCE_GLOB=$(wildcard bin/*.py src/**/*.py tests/**/*.py examples/*.py)

#
# Huan(202003)
# 	F811: https://github.com/PyCQA/pyflakes/issues/320#issuecomment-469337000
#
IGNORE_PEP=E203,E221,E241,E272,E501,F811

# help scripts to find the right place of wechaty module
export PYTHONPATH=src/

.PHONY: all
all : clean lint

.PHONY: clean
clean:
	rm -fr dist/*

.PHONY: lint
lint: pylint pycodestyle flake8 mypy pytype


# disable: TODO list temporay
.PHONY: pylint
pylint:
	pylint \
		--load-plugins pylint_quotes \
		--disable=W0511,R0801 \
		$(SOURCE_GLOB)

.PHONY: pycodestyle
pycodestyle:
	pycodestyle \
		--statistics \
		--count \
		--ignore="${IGNORE_PEP}" \
		$(SOURCE_GLOB)

.PHONY: flake8
flake8:
	flake8 \
		--ignore="${IGNORE_PEP}" \
		$(SOURCE_GLOB)

.PHONY: mypy
mypy:
	MYPYPATH=stubs/ mypy \
		$(SOURCE_GLOB)

.PHONE: pytype
pytype:
	pytype src/ --disable=import-error,pyi-error
	pytype examples/ --disable=import-error

.PHONY: install
install:
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt

.PHONY: pytest
pytest:
	pytest src/ tests/

.PHONY: test-unit
test-unit: pytest

.PHONY: test
test: check-version lint pytest

.PHONY: check-version
check-version:
	./scripts/check_version.py

code:
	code .

.PHONY: run
run:
	python3 bin/run.py

.PHONY: dist
dist:
	python3 setup.py sdist bdist_wheel

.PHONY: publish
publish:
	PATH=~/.local/bin:${PATH} twine upload dist/*

.PHONY: bot
bot:
	python3 examples/ding-dong-bot.py

.PHONY: version
version:
	@newVersion=$$(awk -F. '{print $$1"."$$2"."$$3+1}' < VERSION) \
		&& echo $${newVersion} > VERSION \
		&& echo VERSION = \'$${newVersion}\' > src/version.py \
		&& git add VERSION src/version.py \
		&& git commit -m "$${newVersion}" > /dev/null \
		&& git tag "v$${newVersion}" \
		&& echo "Bumped version to $${newVersion}"
