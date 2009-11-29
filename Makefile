DEV_SERVER=../google_appengine/dev_appserver.py

all:
	python2.5 $(DEV_SERVER) .

count-loc:
	py.countloc model ui generators

dbview:
	dia doc/database.dia -e /tmp/database.png
	eog /tmp/database.png

clean:
	-rm index.yaml
	-rm beautybar.pyc
	-rm `find model ui generators lib -regex .*pyc`
