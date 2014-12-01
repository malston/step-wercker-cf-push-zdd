from pyvows import Vows, expect
from app_info import AppInfo
from config import Config
import re
import json

cfg = Config()
ORGFILE = "fixtures/orgs.json"
SPACEFILE = "fixtures/spaces.json"
ROUTEFILE = "fixtures/routes.json"
APPFILE = "fixtures/apps.json"
APPNAME = "sample-todo"
KNOWN_EXPRESSIONS = [ 
  {
    "rgx": re.compile("cf curl /v2/organizations -X 'GET'"),
    "name": ORGFILE
  },
  {
    "rgx": re.compile("cf curl /v2/organizations/.*/spaces -X 'GET'"),
    "name": SPACEFILE
  },
  {
    "rgx": re.compile("cf curl /v2/spaces/.*/routes -X 'GET'"),
    "name": ROUTEFILE
  },
  {
    "rgx": re.compile("cf curl /v2/routes/.*/apps -X 'GET'"),
    "name": APPFILE
  }
]

def mock_success_sys_call(cmd_str):
  return_string = ""

  for i in KNOWN_EXPRESSIONS:
    if i["rgx"].match(cmd_str) != None:
      return_string = _get_filestring(i["name"])

  return (return_string, False)

def mock_failure_sys_call(cmd_str):
  return (cmd_str, True)

def _get_filestring(filename):
  data = ""

  with open(filename, "r") as myfile:
    data=myfile.read().replace('\n', '')

  return data

@Vows.batch
class ModuleTestsForAppInfo(Vows.Context):
  def topic(self):
    env = {}
    env[cfg.make_name(cfg.ORG)] = "pivotalservices"
    env[cfg.make_name(cfg.SPACE)] = "development"
    env[cfg.make_name(cfg.APP_NAME)] = APPNAME
    env[cfg.make_name(cfg.HOST)] = APPNAME
    return env

  class WhenGettingRoutingTableSuccessfully(Vows.Context):
    ENV_VAR = {}
    def topic(self, env):
      self.ENV_VAR = env
      app_info = AppInfo( system_call=mock_success_sys_call,
                          env_variables=env,
                          cf_cmd="cf")
      return app_info

    def we_get_a_error_value_of_False(self, topic):
      app_info = topic
      expect(app_info).Not.to_be_null() 

    def get_existing_app_details_should_yield_json(self, topic):
      app_info = topic
      _, new_app_name, app_name = cfg.get_app_name(self.ENV_VAR)
      app_file_json = json.loads(_get_filestring(APPFILE))
      app_details_control = [x["entity"] for x in app_file_json["resources"] if x["entity"]["name"] != new_app_name]
      app_details, err = app_info.get_existing_app_details()
      expect(app_details).to_equal(app_details_control)
      expect(len(set(err))).to_equal(1)
      expect(False in set(err)).to_equal(True)








