.PHONY: build clean dev_deps

dev_deps:
	pip3 install -r dev_requirements.txt

build: dev_deps
	python3 setup.py sdist
	python3 setup.py bdist_wheel

clean:
	rm -rf build dist

releasetest: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

viewreleasetest: b
	xdg-open https://testpypi.python.org/pypi/pathaliases

release: build
	twine upload dist/*
