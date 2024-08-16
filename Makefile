install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-reinstall:
	python3 -m pip install --force-reinstall --user dist/*.whl

def:
	poetry run flask --app page_analyzer:app run

lint:
	poetry run flake8 page_nalyzer

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml tests/

PORT &= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_alayzer:app
