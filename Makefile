.PHONY: test setup detect doctor install

test:
	python3 -m pytest -q

setup:
	./setup.sh

detect:
	python3 setup.py detect --write --no-spinner

doctor:
	python3 setup.py doctor --no-spinner

install:
	python3 setup.py install --no-spinner
