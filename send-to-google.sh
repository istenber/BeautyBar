#!/bin/sh

APP_FILE=app.yaml
TMP_FOLDER=/tmp/export
APP_ENGINE_PATH=/home/sankari/dev/google_appengine/
COMPRESS_JAR=/home/sankari/dev/beautybar/utils/yuicompressor-2.4.2.jar
GIT_REPO=file:///home/sankari/dev/beautybar/.git/
JS_FILE=beautybar/static/js/beautybar.js
CSS_FILE=beautybar/static/css/screen.css

# increase version number in app.yaml
NEW_VERSION=`awk '/^version/ {print $2+1;}' ${APP_FILE}`
MSG="Sending version $NEW_VERSION to Google"
echo $MSG
TMP_FILE=/tmp/app.yaml.tmp
sed 's/^version: .*$/version: 7/' ${APP_FILE} > ${TMP_FILE}
mv ${TMP_FILE} ${APP_FILE}

# commiting new version file
git commit -m "${MSG}" ${APP_FILE}

# making temp export folder
rm -rf ${TMP_FOLDER}
mkdir -p ${TMP_FOLDER}

# exporting git repo and remove unneeded files
git clone ${GIT_REPO} ${TMP_FOLDER}/beautybar
rm -rf ${TMP_FOLDER}/beautybar/.git
rm -rf ${TMP_FOLDER}/beautybar/doc
rm -rf ${TMP_FOLDER}/beautybar/tests
# TODO: do not remove or everything will blow
# rm -rf ${TMP_FOLDER}/beautybar/ui/test
rm ${TMP_FOLDER}/beautybar/README
rm ${TMP_FOLDER}/beautybar/generators/skel.py
rm ${TMP_FOLDER}/beautybar/send-to-google.sh

# obfuscate and compress javascript code
TMP_FILE=/tmp/js.compressed
java -jar ${COMPRESS_JAR} --type js -o ${TMP_FILE} ${TMP_FOLDER}/${JS_FILE}
mv ${TMP_FILE} ${TMP_FOLDER}/${JS_FILE}

# obfuscate and compress css code
TMP_FILE=/tmp/css.compressed
java -jar ${COMPRESS_JAR} --type css -o ${TMP_FILE} ${TMP_FOLDER}/${CSS_FILE}
mv ${TMP_FILE} ${TMP_FOLDER}/${CSS_FILE}

# send to google
${APP_ENGINE_PATH}/appcfg.py update ${TMP_FOLDER}/beautybar
echo "select new version to active from dashboard"
echo "    https://appengine.google.com/deployment?&app_id=beauty-bar"
