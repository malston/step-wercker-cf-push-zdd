#!/bin/sh

./stage_env.sh

echo "cleaning up"
sudo apt-get purge golang-stable -y
rm -fR /tmp/bin/autopilot
rm -fR ./cf

