.PHONY: all

SRC := ./src
CMD := poetry run

all: install-deps pre-commit test

test:
	$(CMD) pytest

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	poetry install
	$(CMD) pre-commit install
