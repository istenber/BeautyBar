DEV_SERVER=../google_appengine/dev_appserver.py

all:
	python2.5 $(DEV_SERVER) .

apidoc:
	-mkdir apidoc
	epydoc -o apidoc beautybar.py model ui generators
	@echo "open apidoc/index.html"

count-loc:
	py.countloc model ui generators

test:
	PYTHONPATH=$(PWD) python2.5 `which py.test` tests

dbview:
	dia doc/database.dia -e /tmp/database.png
	eog /tmp/database.png

clean:
	-rm index.yaml
	-rm beautybar.pyc
	-rm `find model ui generators lib -regex .*pyc`
	-rm -rf apidoc
