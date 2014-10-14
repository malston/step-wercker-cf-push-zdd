from pyvows import Vows, expect
from app_info import AppInfo
from config import Config

cfg = Config()

def mock_success_sys_call(cmd_str):
  print("Success Mock: ", cmd_str)
  return (cmd_str, False)

def mock_failure_sys_call(cmd_str):
  print("Fail Mock: ",cmd_str)
  return (cmd_str, True)

@Vows.batch
class ModuleTestsForAppInfo(Vows.Context):
  def topic(self):
    env = {}
    env[cfg.make_name(cfg.ORG)] = "pivotalservices"
    env[cfg.make_name(cfg.SPACE)] = "development"
    env[cfg.make_name(cfg.APP_NAME)] = "mytestapp"
    return env

  class WhenGettingRoutingTableSuccessfully(Vows.Context):
    def topic(self, env):
      app_info = AppInfo( system_call=mock_success_sys_call,
                          env_variables=env )
      return ({}, False)

    def we_get_a_False_error_value(self, topic):
      push_string, err = topic
      expect(err).to_equal(False) 
