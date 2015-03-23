#!/bin/sh

sudo apt-get install -y python wget
wget http://go-cli.s3-website-us-east-1.amazonaws.com/releases/v6.3.2/cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz
export CF_CLI=$(pwd)/cf

(cd $WERCKER_STEP_ROOT && python run.py)

if [ $? != 0 ]; then
  fail "Failure"

else
  success "Success"
fi
