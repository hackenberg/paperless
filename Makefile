FLASK_APP := paperless
FLASK_ENV := development

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK := env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) $(VENV)/bin/flask
PYTEST := $(VENV)/bin/pytest
COVERAGE := $(VENV)/bin/coverage

JQUERY := https://code.jquery.com/jquery-3.4.1
BOOTSTRAP := https://github.com/twbs/bootstrap/releases/download/v4.4.1/bootstrap-4.4.1-dist.zip

lint:
	flake8 paperless/*.py tests/*.py

run: $(VENV) instance/dev.sqlite instance/jquery instance/bootstrap
	$(FLASK) run

.PHONY: lint run

instance/dev.sqlite: $(VENV)
	$(FLASK) init-db

instance/jquery:
	mkdir -p $@
	wget -O $@/jquery.js $(JQUERY).js
	wget -O $@/jquery.min.js $(JQUERY).min.js
	wget -O $@/jquery.min.map $(JQUERY).min.map
	cp -r $@ paperless/static/

instance/bootstrap: instance/bootstrap-4.4.1-dist.zip
	mkdir -p $@
	unzip $^
	mv bootstrap-4.4.1-dist/* $@
	rmdir bootstrap-4.4.1-dist
	cp -r $@ paperless/static/

instance/bootstrap-4.4.1-dist.zip:
	mkdir -p $(dir $@)
	wget -O $@ $(BOOTSTRAP)

clean:
	rm -rf \
		build/ \
		instance/bootstrap/ \
		paperless/static/{bootstrap,jquery}/ \
		paperless/__pycache__/ \
		tests/__pycache__/ \
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

$(VENV):
	python -m venv $@
