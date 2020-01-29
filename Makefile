FLASK_APP := paperless
FLASK_ENV := development

init-db:
	env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask init-db

run:
	env FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run

deps: bootstrap-4.4.1-dist.zip jquery-3.4.1.js

jquery-3.4.1.min.js:
	wget https://code.jquery.com/$@

jquery-3.4.1.min.map:
	wget https://code.jquery.com/$@

jquery-3.4.1.js:
	wget https://code.jquery.com/$@

bootstrap-4.4.1-dist.zip:
	wget https://github.com/twbs/bootstrap/releases/download/v4.4.1/$@

.PHONY: init-db run
