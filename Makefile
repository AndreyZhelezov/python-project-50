install:
	poetry install

check:
	poetry run flake8 gendiff
	poetry run pytest

test-coverage:
	poetry run pytest --cov --cov-report xml

.PHONY: check