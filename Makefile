.PHONY: all

CMD := poetry run

INTEGRATION_TESTS := ./tests/integration
UNIT_TESTS := ./tests/unit

all: install-deps pre-commit test

test: test-unit test-integration

test-unit:
	$(CMD) pytest -vv $(UNIT_TESTS)

test-integration:
	$(CMD) pytest -vv $(INTEGRATION_TESTS)

pre-commit:
	$(CMD) pre-commit run --all-files

install-deps:
	@poetry install
	$(CMD) pre-commit install

run-server:
	$(CMD) python -m src.main
