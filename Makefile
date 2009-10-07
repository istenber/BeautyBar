DEV_SERVER="../app-engine/dev_appserver.py"


all:
	python2.5 $(DEV_SERVER) .

clean:
	-rm index.yaml
	-rm `find . -regex .*pyc`