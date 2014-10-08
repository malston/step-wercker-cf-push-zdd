#!/bin/sh

sudo apt-get install -y python
wget http://go-cli.s3-website-us-east-1.amazonaws.com/releases/v6.3.2/cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz

python $WERCKER_STEP_ROOT/run.py

if [ $? != 0 ]; then
  fail "Failure"

else
  success "Success"
fi


#check_variables=$(python run.py)
#exitcode= `echo $?`
#checkFailure $check_variables $exitcode
#set -e
#CF=./cf

#${CF} api ${WERCKER_CF_PUSH_CLOUDFOUNDRY_API_URL}
#${CF} login -u ${WERCKER_CF_PUSH_CLOUDFOUNDRY_USER_NAME} -p ${WERCKER_CF_PUSH_CLOUDFOUNDRY_USER_PASS} -o ${WERCKER_CF_PUSH_CLOUDFOUNDRY_ORG} -s ${WERCKER_CF_PUSH_CLOUDFOUNDRY_SPACE}

#WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME_NEW=${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME}-zdd-${WERCKER_GIT_COMMIT}
#APPINFO=`cf curl /v2/apps -X GET | python json_parser.py ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME}-zdd`
#PUSH_CMD=""

#PUSH_CMD="${CF} push ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME_NEW}"

#if [ ${WERCKER_CF_PUSH_CLOUDFOUNDRY_USE_MANIFEST} == false ]; then
  #PUSH_CMD="${PUSH_CMD} --no-manifest"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_BUILDPACK} ]; then
  #PUSH_CMD="${PUSH_CMD} -b ${WERCKER_CF_PUSH_CLOUDFOUNDRY_BUILDPACK}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_COMMAND} ]; then
  #PUSH_CMD="${PUSH_CMD} -c ${WERCKER_CF_PUSH_CLOUDFOUNDRY_COMMAND}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_DOMAIN} ]; then
  #PUSH_CMD="${PUSH_CMD} -d ${WERCKER_CF_PUSH_CLOUDFOUNDRY_DOMAIN}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NUM_INSTANCES} ]; then
  #PUSH_CMD="${PUSH_CMD} -i ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NUM_INSTANCES}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_MEMORY} ]; then
  #PUSH_CMD="${PUSH_CMD} -m ${WERCKER_CF_PUSH_CLOUDFOUNDRY_MEMORY}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_HOST} ]; then
  #PUSH_CMD="${PUSH_CMD} -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_HOST}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_PATH} ]; then
  #PUSH_CMD="${PUSH_CMD} -p ${WERCKER_CF_PUSH_CLOUDFOUNDRY_PATH}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_STACK} ]; then
  #PUSH_CMD="${PUSH_CMD} -s ${WERCKER_CF_PUSH_CLOUDFOUNDRY_STACK}"
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_HOSTNAME} ]; then
  #if [ ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_HOSTNAME} == true ]; then
    #PUSH_CMD="${PUSH_CMD} --no-hostname"
  #fi
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_ROUTE} ]; then
  #if [ ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_ROUTE} == true]; then
    #PUSH_CMD="${PUSH_CMD} --no-route"
  #fi
#fi

#if [ -n ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_START} ]; then
  #if [ ${WERCKER_CF_PUSH_CLOUDFOUNDRY_NO_START} == true ]; then
    #PUSH_CMD="${PUSH_CMD} --no-start"
  #fi
#fi

#set +e
#push_output=$($PUSH_CMD)
#checkFailure $push_output $?
#echo 'finished pushing to cloudfoundry';
#set -e

#if [ ${APPINFO} == "notfound" ]; then
  #cf create-route ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME}
#fi
#cf map-route ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME_NEW} ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME}

#set +e
#push_output=$(if [ ${APPINFO} != "notfound" ]; then
  #APPNAME=`echo ${APPINFO} | awk -F"|" '{print $1}'`
  #APPINSTANCES=`echo ${APPINFO} | awk -F"|" '{print $2}'`
  #APPMEM=`echo ${APPINFO} | awk -F"|" '{print $3}'`
  #APPDISK=`echo ${APPINFO} | awk -F"|" '{print $4}'`
  #yes | cf scale ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME_NEW} -i ${APPINSTANCES} -m ${APPMEM} -k ${APPDISK}
  #yes | cf unmap-route ${APPNAME} ${WERCKER_CF_PUSH_CLOUDFOUNDRY_APP_NAME}
  #yes | cf stop ${APPNAME}
#fi)

#checkFailure $push_output $?
#success 'finished pushing to cloudfoundry';

#set -e
