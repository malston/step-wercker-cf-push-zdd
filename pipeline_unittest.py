from pyvows import Vows, expect
from pipeline import execute
from config import Config

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)
SUCCESS_CONTROL_MSG = "success_message"
FAILURE_CONTROL_MSG = "failure_message"

def mock_system_call_success(cmd_string):
  print("Running cmd: {0}".format(cmd_string))
  return (SUCCESS_CONTROL_MSG, False)

def mock_system_call_failure(cmd_string):
  print("Running cmd: {0}".format(cmd_string))
  return (FAILURE_CONTROL_MSG, True)

def get_di(env_vars, pfx, sys_call):
  rfc_di = {}
  rfc_di[cfg.ENV_VARIABLES] = env_vars
  rfc_di[cfg.VARIABLE_PREFIX] = pfx
  rfc_di[cfg.SYS_CALL] = sys_call
  rfc_di[cfg.CF_CMD] = "./cf"
  return rfc_di

def setup_env(hash):
  ENV_VARIABLES = {}
  ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "false"
  ENV_VARIABLES[cfg.make_name(cfg.SPACE)] = "some-space"
  ENV_VARIABLES[cfg.make_name(cfg.APP_NAME)] = "my_test_app"
  ENV_VARIABLES["WERCKER_GIT_COMMIT"] = hash
  return ENV_VARIABLES

@Vows.batch
class ModuleTestsForPipeline(Vows.Context):
  class PipelineSuccesfulCalls(Vows.Context):
    def topic(self):
      ENV_VARIABLES = setup_env("pipeline_unittest_commit_hash_success")
      run_di = get_di(ENV_VARIABLES, PREFIX, mock_system_call_success)
      return execute( **run_di )

    def we_get_a_False_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(False)

    def we_get_the_successful_command_output(self, topic):
      msg, err = topic
      expect(msg).to_equal(SUCCESS_CONTROL_MSG)

  class PipelineFailingCalls(Vows.Context):
    def topic(self):
      ENV_VARIABLES = setup_env("pipeline_unittest_commit_hash_failure")
      run_di = get_di(ENV_VARIABLES, PREFIX, mock_system_call_failure)
      return execute( **run_di )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

    def we_get_a_Error_message(self, topic):
      msg, err = topic
      expect(msg).to_equal(FAILURE_CONTROL_MSG)
