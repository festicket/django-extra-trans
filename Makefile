help:
	@echo "install - install the project from scratch. You need to specify python version to use."
	@echo "test-all - a shorcut to run all the tests."

install:
	$(python) -m venv venv && \
	. venv/bin/activate && \
	python -m pip install -r requirements.txt && \
	cd example && \
	python manage.py migrate


make test-all:
	. venv/bin/activate && cd example && pytest
