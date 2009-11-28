#!/bin/sh


APP_FILE=app.yaml
TMP_FOLDER=/tmp/export
APP_ENGINE_PATH=/home/sankari/dev/google_appengine/
JSO_JAR=/home/sankari/dev/google_appengine/utils/jso.jar
JS_FILE=static/js/beautybar.js

# increase version number in app.yaml
NEW_VERSION=`awk '/^version/ {print $2+1;}' ${APP_FILE}`
echo $MSG
sed 's/^version: .*$/version: 7/' ${APP_FILE} > /tmp/${APP_FILE}
mv /tmp/${APP_FILE} ${APP_FILE}

git commit -m $MSG ${APP_FILE}

# making temp export folder
mkdir ${TMP_FOLDER}
cd ${TMP_FOLDER}
CURDIR=`pwd`
if [ "x${CURDIR}" != "x${TMP_FOLDER" ]; then
    echo "cannot make temp dir, exiting."
    exit 1
fi

# exporting git repo and remove unneeded files
git clone file:///home/sankari/dev/beautybar/.git/ beautybar
rm -rf beautybar/.git
rm -rf beautybar/doc
rm beautybar/README

# obfuscate javascript code
TMP_FILE=/tmp/obf.js.tmp
java -jar ${JSO_JAR} ${JS_FILE} > ${TMP_FILE}
mv ${TMP_FILE} ${JS_FILE}

MSG="Sending version $NEW_VERSION to Google"
${APP_ENGINE_PATH}/appcfg.py update beautybar

echo "select new version to active from dashboard"
echo "    https://appengine.google.com/deployment?&app_id=beauty-bar"
