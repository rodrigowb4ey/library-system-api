.PHONY: install format lint

install:
	@poetry install
format:
	@isort .
	@blue .
lint:
	@blue . --check
	@isort . --check