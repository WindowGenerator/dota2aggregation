.PHONY: all

CMD := poetry run

all: install-deps pre-commit test

test:
	$(CMD) pytest -vv

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	@poetry install
	$(CMD) pre-commit install

run-server:
	$(CMD) python -m src.main
