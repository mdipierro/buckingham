clean:
	rm -rf dist
build:
	make clean
	python setup.py build
install: dist
	python setup.py install
test:	install
	python -m unittest tests.test_simple
deploy:
	make clean
	#http://guide.python-distribute.org/creation.html
	python setup.py sdist
	twine upload dist/*
