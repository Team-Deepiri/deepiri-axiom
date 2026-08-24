.PHONY: test setup detect doctor install

test:
	python3 -m pytest -q

setup install:
	./install.sh

detect:
	./install.sh detect --write

doctor:
	./install.sh doctor
