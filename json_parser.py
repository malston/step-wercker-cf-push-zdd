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

def findAppNameMatch(appNameArg, name):
  return re.match( appNameArg+'-([0-9a-f]{5,40})', name, re.M|re.I)

def appIsRunning(state):
  return state != "STOPPED"

def iterateJson(appNameArg, jsonObj):
  rval = "notfound"

  if "resources" in jsonObj:
    for i in jsonObj["resources"]:
      e = i["entity"]
      name = e["name"]

      if findAppNameMatch(appNameArg, name) and appIsRunning(e["state"]):
        rval = str(name)+"|"+str(e["instances"])+"|"+str(e["memory"])+"|"+str(e["disk_quota"])
        break

  return rval

def getApp():
    appNameArg = sys.argv[1]
    j = getJsonObject()
    return iterateJson(appNameArg, j)

if __name__ == '__main__':
  print(getApp())
