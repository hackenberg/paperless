FLASK_APP := paperless
FLASK_ENV := development

JQUERY := https://code.jquery.com/jquery-3.4.1
BOOTSTRAP := https://github.com/twbs/bootstrap/releases/download/v4.4.1/bootstrap-4.4.1-dist.zip

lint:
	flake8 paperless/*.py

init-db:
	env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask init-db

run: instance/jquery instance/bootstrap
	env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run

.PHONY: lint init-db run

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
	rm -rf instance/bootstrap paperless/static/{bootstrap,jquery}

.PHONY: clean
