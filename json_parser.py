import json
import sys
import re

jsonStr = ""

for line in sys.stdin:
  jsonStr += line

j = json.loads(jsonStr)

def getApp(j):
    rval = "notfound"

    for i in j["resources"]:
        e = i["entity"]
        matchObj = re.match( sys.argv[1]+'-([0-9a-f]{5,40})', e["name"], re.M|re.I)
        
        if matchObj and e["state"] != "STOPPED":
            rval = str(e["name"])+"|"+str(e["instances"])+"|"+str(e["memory"])+"|"+str(e["disk_quota"])
            break

    return rval
print(getApp(j))
