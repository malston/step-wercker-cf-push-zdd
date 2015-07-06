#!/bin/sh
if [ ! -n "$WERCKER_CF_PUSH_ZDD_API_URL" ]
then
    fail 'missing or empty option api_url, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_APP_NAME" ]
then
    fail 'missing or empty option app_name, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_USER_NAME" ]
then
    fail 'missing or empty option user_name, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_USER_PASS" ]
then
    fail 'missing or empty option user_pass, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_ORG" ]
then
    fail 'missing or empty option org, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_SPACE" ]
then
    fail 'missing or empty option space, please check wercker.yml'
fi

if [ ! -n "$WERCKER_CF_PUSH_ZDD_USE_MANIFEST" ]
then
    fail 'missing or empty option use_manifest, please check wercker.yml'
fi

sudo apt-get install -y golang
wget http://go-cli.s3-website-us-east-1.amazonaws.com/releases/v6.3.2/cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz
CF=./cf
${CF} api ${WERCKER_CF_PUSH_ZDD_API_URL}

${CF} login -u ${WERCKER_CF_PUSH_ZDD_USER_NAME} -p ${WERCKER_CF_PUSH_ZDD_USER_PASS} -o ${WERCKER_CF_PUSH_ZDD_ORG} -s ${WERCKER_CF_PUSH_ZDD_SPACE}

go get github.com/xchapter7x/autopilot
${CF} install-plugin $GOPATH/bin/autopilot

PUSH_CMD=""
PUSH_CMD="${CF} push-zdd ${WERCKER_CF_PUSH_ZDD_APP_NAME}"

if [[ ${WERCKER_CF_PUSH_ZDD_USE_MANIFEST} == false ]]; then
  PUSH_CMD="${PUSH_CMD} --no-manifest"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_BUILDPACK} ]; then
  PUSH_CMD="${PUSH_CMD} -b ${WERCKER_CF_PUSH_ZDD_BUILDPACK}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_COMMAND} ]; then
  PUSH_CMD="${PUSH_CMD} -c ${WERCKER_CF_PUSH_ZDD_COMMAND}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_DOMAIN} ]; then
  PUSH_CMD="${PUSH_CMD} -d ${WERCKER_CF_PUSH_ZDD_DOMAIN}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_NUM_INSTANCES} ]; then
  PUSH_CMD="${PUSH_CMD} -i ${WERCKER_CF_PUSH_ZDD_NUM_INSTANCES}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_MEMORY} ]; then
  PUSH_CMD="${PUSH_CMD} -m ${WERCKER_CF_PUSH_ZDD_MEMORY}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_HOST} ]; then
  WERCKER_CF_PUSH_ZDD_HOST=`echo ${WERCKER_CF_PUSH_ZDD_HOST} | tr "\/" "-" | tr "\." "-"`
  PUSH_CMD="${PUSH_CMD} -n ${WERCKER_CF_PUSH_ZDD_HOST}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_PATH} ]; then
  PUSH_CMD="${PUSH_CMD} -p ${WERCKER_CF_PUSH_ZDD_PATH}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_STACK} ]; then
  PUSH_CMD="${PUSH_CMD} -s ${WERCKER_CF_PUSH_ZDD_STACK}"
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_NO_HOSTNAME} ]; then
  if [[ ${WERCKER_CF_PUSH_ZDD_NO_HOSTNAME} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-hostname"
  fi
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_NO_ROUTE} ]; then
  if [[ ${WERCKER_CF_PUSH_ZDD_NO_ROUTE} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-route"
  fi
fi

if [ ! -z ${WERCKER_CF_PUSH_ZDD_NO_START} ]; then
  if [[ ${WERCKER_CF_PUSH_ZDD_NO_START} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-start"
  fi
fi

echo "$PUSH_CMD"

sudo $PUSH_CMD

if [[ $? -ne 0 ]];then
    warning $push_output
    fail 'push failed';

else
    success 'finished pushing to cloudfoundry';

fi

