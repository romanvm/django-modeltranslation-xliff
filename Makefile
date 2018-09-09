.PHONY: server, test, pdb-test, coverage, clean, build, upload

server:
	python manage.py runserver

test:
	pytest -vv

pdb-test:
	pytest -x --pdb

coverage:
	pytest --cov modeltranslation_xliff --cov-report term --cov-report html

clean:
	rm -rf ./build
	rm -rf ./dist

build:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*
