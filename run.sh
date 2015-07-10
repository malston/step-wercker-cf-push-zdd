#!/bin/sh
fail () {
  echo $1
  exit 1
}

if [ ! -n "$ZDD_API_URL" ]
then
    fail 'missing or empty option api_url, please check ENV Vars'
fi

if [ ! -n "$ZDD_APP_NAME" ]
then
    fail 'missing or empty option app_name, please check ENV Vars'
fi

if [ ! -n "$ZDD_USER_NAME" ]
then
    fail 'missing or empty option user_name, please check ENV Vars'
fi

if [ ! -n "$ZDD_USER_PASS" ]
then
    fail 'missing or empty option user_pass, please check ENV Vars'
fi

if [ ! -n "$ZDD_ORG" ]
then
    fail 'missing or empty option org, please check ENV Vars'
fi

if [ ! -n "$ZDD_SPACE" ]
then
    fail 'missing or empty option space, please check ENV Vars'
fi

if [ ! -n "$ZDD_USE_MANIFEST" ]
then
    fail 'missing or empty option use_manifest, please check ENV Vars'
fi

./stage_env.sh
CF=./cf

echo "running cf api ${ZDD_API_URL} command"
${CF} api ${ZDD_API_URL}

echo "running ${CF} login -u ${ZDD_USER_NAME} -p ###### -o ${ZDD_ORG} -s ${ZDD_SPACE} command"
${CF} login -u ${ZDD_USER_NAME} -p ${ZDD_USER_PASS} -o ${ZDD_ORG} -s ${ZDD_SPACE}

PUSH_CMD=""
PUSH_CMD="${CF} push-zdd ${ZDD_APP_NAME}"

if [[ ${ZDD_USE_MANIFEST} == false ]]; then
  PUSH_CMD="${PUSH_CMD} --no-manifest"
fi

if [ ! -z ${ZDD_BUILDPACK} ]; then
  PUSH_CMD="${PUSH_CMD} -b ${ZDD_BUILDPACK}"
fi

if [ ! -z ${ZDD_COMMAND} ]; then
  PUSH_CMD="${PUSH_CMD} -c ${ZDD_COMMAND}"
fi

if [ ! -z ${ZDD_DOMAIN} ]; then
  PUSH_CMD="${PUSH_CMD} -d ${ZDD_DOMAIN}"
fi

if [ ! -z ${ZDD_NUM_INSTANCES} ]; then
  PUSH_CMD="${PUSH_CMD} -i ${ZDD_NUM_INSTANCES}"
fi

if [ ! -z ${ZDD_MEMORY} ]; then
  PUSH_CMD="${PUSH_CMD} -m ${ZDD_MEMORY}"
fi

if [ ! -z ${ZDD_HOST} ]; then
  ZDD_HOST=`echo ${ZDD_HOST} | tr "\/" "-" | tr "\." "-"`
  PUSH_CMD="${PUSH_CMD} -n ${ZDD_HOST}"
fi

if [ ! -z ${ZDD_PATH} ]; then
  PUSH_CMD="${PUSH_CMD} -p ${ZDD_PATH}"
fi

if [ ! -z ${ZDD_STACK} ]; then
  PUSH_CMD="${PUSH_CMD} -s ${ZDD_STACK}"
fi

if [ ! -z ${ZDD_NO_HOSTNAME} ]; then
  if [[ ${ZDD_NO_HOSTNAME} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-hostname"
  fi
fi

if [ ! -z ${ZDD_NO_ROUTE} ]; then
  if [[ ${ZDD_NO_ROUTE} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-route"
  fi
fi

if [ ! -z ${ZDD_NO_START} ]; then
  if [[ ${ZDD_NO_START} == true ]]; then
    PUSH_CMD="${PUSH_CMD} --no-start"
  fi
fi

echo "$PUSH_CMD"

sudo $PUSH_CMD

if [[ $? -ne 0 ]];then
    echo $push_output
    fail 'push failed';

else
    echo 'finished pushing to cloudfoundry';
    exit 0;
fi

