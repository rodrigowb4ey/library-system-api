.PHONY: install format lint

install:
	@poetry install
format:
	@isort .
	@blue .
lint:
	@isort . --check
	@blue . --check