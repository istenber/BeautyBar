DEV_SERVER=../google_appengine/dev_appserver.py
JS_FILE=static/js/beautybar.js

all:
	python2.5 $(DEV_SERVER) .

dbview:
	dia doc/database.dia -e /tmp/database.png
	eog /tmp/database.png

obfusc-js:
	# obfuscator got from http://www.shaneng.net/Main/JavaScriptObfuscator
	java -jar utils/jso.jar $(JS_FILE) > $(JS_FILE)-obfs

update:
	@echo "1. edit app.yaml: add version number 1"
	@echo "2. make clean clone?"
	@echo "    git clone file:///home/sankari/dev/beautybar/.git/ beautybar"
	@echo "3. run PATH/google_appengine/appcfg.py update beautybar"
	@echo "4. select new version to active from dashboard"
	@echo "    https://appengine.google.com/deployment?&app_id=beauty-bar"

clean:
	-rm index.yaml
	-rm `find . -regex .*pyc`
