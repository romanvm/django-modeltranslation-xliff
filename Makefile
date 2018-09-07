.PHONY: server, test, coverage, upload

server:
	python manage.py runserver

test:
	pytest -vv

coverage:
	pytest --cov modeltranslation_xliff --cov-report term --cov-report html

upload:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
