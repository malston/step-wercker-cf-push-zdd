import json
import sys
import re

def stdinGen():
  for line in sys.stdin:
    yield line

def readPipeAsString():
  return ''.join(stdinGen())

def getJsonObject():
  return json.loads(readPipeAsString())

def findAppNameMatch(name):
  return re.match( sys.argv[1]+'-([0-9a-f]{5,40})', name, re.M|re.I)

def appIsRunning(state):
  return state != "STOPPED"

def getApp():
    j = getJsonObject()
    rval = "notfound"

    for i in j["resources"]:
        e = i["entity"]
        name = e["name"]

        if findAppNameMatch(name) and appIsRunning(e["state"]):
            rval = str(name)+"|"+str(e["instances"])+"|"+str(e["memory"])+"|"+str(e["disk_quota"])
            break

    return rval

print(getApp())
