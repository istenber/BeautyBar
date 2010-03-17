#!/bin/sh

APP_FILE=app.yaml
TMP_FOLDER=/tmp/export
APP_ENGINE_PATH=$PWD/../google_appengine/
GIT_REPO=file://$PWD/.git/

PARAM=$1

if [ "x$PARAM" = "x--help" ]; then
    echo "Usage: send-to-google.sh [-new-version]"
    echo " if -new-version parameter is used version is increased"
    exit 1
fi

# various checks...
GIT_STATUS=`git st`

BRANCH_OK=`echo $GIT_STATUS | grep "# On branch master"`
if ! [ $? -eq 0 ]; then
    echo "Working directory not ok, exiting..."
    exit 4
fi

COMMIT_OK=`echo $GIT_STATUS | grep "# Changed but not updated:"`
if [ $? -eq 0 ]; then
    echo "Please commit changes before sending, exiting..."
    exit 3
fi

until [ "x$value" = "xy" ] || [ "x$value" = "xn" ]; do
    echo "Do you really want to send app to Google [y|n]?"
    read value
done

if [ "x$value" = "xn" ]; then
    echo "Send cancelled."
    exit 2
fi

# increase version number in app.yaml
if [ "x$PARAM" = "x-new-version" ]; then
    NEW_VERSION=`awk '/^version/ {print $2+1;}' ${APP_FILE}`
    echo "Sending version new version ($NEW_VERSION) to Google"
    TMP_FILE=/tmp/app.yaml.tmp
    sed "s/^version: .*$/version: $NEW_VERSION/" ${APP_FILE} > ${TMP_FILE}
    mv ${TMP_FILE} ${APP_FILE}
    git add ${APP_FILE}
else
    echo "Sending app to Google"
fi

# lets make time stamp like this
date > UPDATED
git add UPDATED

# commiting new version file
git commit -m "Sending app to Google"

# making temp export folder
rm -rf ${TMP_FOLDER}
mkdir -p ${TMP_FOLDER}

# exporting git repo
git clone ${GIT_REPO} ${TMP_FOLDER}/beautybar

# build generator list image and css
CURDIR=`pwd`
cd ${TMP_FOLDER}/beautybar
./montage.sh
cd ${CURDIR}

# remove unneeded files
rm -rf ${TMP_FOLDER}/beautybar/.git
rm -rf ${TMP_FOLDER}/beautybar/doc
rm -rf ${TMP_FOLDER}/beautybar/tests
rm -rf ${TMP_FOLDER}/beautybar/static/js/development
rm ${TMP_FOLDER}/beautybar/README
rm ${TMP_FOLDER}/beautybar/generators/skel.py
rm ${TMP_FOLDER}/beautybar/send-to-google.sh
rm ${TMP_FOLDER}/beautybar/test_model.sh
rm ${TMP_FOLDER}/beautybar/test_browser.sh
rm ${TMP_FOLDER}/beautybar/UPDATED
rm ${TMP_FOLDER}/beautybar/montage.sh

# send to google
${APP_ENGINE_PATH}/appcfg.py update ${TMP_FOLDER}/beautybar

if [ "x$PARAM" = "x-new-version" ]; then
    echo "select new version to active from dashboard"
    echo "    https://appengine.google.com/deployment?&app_id=beauty-bar"
else
    echo "send complete"
fi

exit 0
