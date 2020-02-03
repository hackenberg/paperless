FLASK_APP := paperless
FLASK_ENV := development

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
NPM := yarn
FLASK := env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(VENV)/bin/flask
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage

lint:
	flake8 paperless/*.py tests/*.py

run: $(VENV) instance/dev.sqlite paperless/static/lib
	$(FLASK) run

.PHONY: lint run

instance/dev.sqlite: $(VENV)
	$(FLASK) init-db

$(VENV):
	python -m venv $@

paperless/static/lib: node_modules
	mkdir -p $@
	cp -r $</jquery/dist $@/jquery
	cp -r $</bootstrap/dist $@/bootstrap

node_modules: package.json
	$(NPM) install

clean:
	rm -rf \
		build/ \
		dist/ \
		instance/ \
		node_modules \
		paperless/static/lib/ \
		paperless/__pycache__/ \
		tests/__pycache__/ \
		vent/ \
		*.egg-info

.PHONY: clean

test: $(VENV)
	$(PYTEST)

coverage: $(VENV)
	$(COVERAGE) run -m pytest
	$(COVERAGE) report

install: $(VENV)
	$(PIP) install -e .

.PHONY: test coverage install
