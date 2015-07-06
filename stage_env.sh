#!/bin/sh

sudo add-apt-repository ppa:gophers/go -y
sudo apt-get update -y
sudo apt-get install golang-stable -y

echo ""
echo "lets see if we can setup the environment, plugins and all"
echo ""
wget http://go-cli.s3-website-us-east-1.amazonaws.com/releases/v6.12.0/cf-linux-amd64.tgz
tar -zxvf cf-linux-amd64.tgz
CF=./cf

echo "testing cf command"
${CF} help

echo "go getting autopilot"
GOPATH=/tmp go get github.com/xchapter7x/autopilot
ls -la /tmp

echo "installing autopilot plugin"
${CF} install-plugin /tmp/bin/autopilot
