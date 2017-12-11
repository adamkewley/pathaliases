.PHONY: build clean

build:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

clean:
	rm -rf build dist

releasetest:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

viewreleasetest:
	xdg-open https://testpypi.python.org/pypi/pathaliases

release:
	twine upload dist/*
