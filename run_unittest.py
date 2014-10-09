from pyvows import Vows, expect
from run import run
import os
from config import Config
from make_push_string import make_push_string

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)

def get_di(required_fields, env_vars, pfx, pipeline):
  rfc_di = {}
  rfc_di[cfg.REQUIRED_FIELDS] = required_fields
  rfc_di[cfg.ENV_VARIABLES] = env_vars
  rfc_di[cfg.VARIABLE_PREFIX] = pfx
  rfc_di[cfg.SYS_CALL] = mock_system_call
  rfc_di[cfg.PIPELINE] = pipeline
  rfc_di[cfg.CF_CMD] = "./cf"
  return rfc_di

def mock_system_call(cmd_string):
  return (cmd_string, False)

def mock_pipeline_step(**kwargs):
  return ("success", False)

@Vows.batch
class ModuleTestsForRun(Vows.Context):
  def topic(self):
    rval = []
    rval.append(cfg.MANIFEST)
    rval.append(cfg.SPACE)
    return rval

  class WhenExecutingYieldsError(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      run_di = get_di(required_fields, ENV_VARIABLES, PREFIX, [])
      return run( **run_di )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenEmptyPipeline(Vows.Context):
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      ENV_VARIABLES[cfg.make_name(cfg.SPACE)] = "some-space"
      ENV_VARIABLES[cfg.make_name(cfg.APP_NAME)] = "my_test_app"
      ENV_VARIABLES["WERCKER_GIT_COMMIT"] = "run_unittest_commit_hash"
      run_di = get_di(required_fields, ENV_VARIABLES, PREFIX, [])
      return run( **run_di )
    
    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingYieldsSuccess(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      ENV_VARIABLES[cfg.make_name(cfg.SPACE)] = "some-space"
      ENV_VARIABLES[cfg.make_name(cfg.APP_NAME)] = "my_test_app"
      ENV_VARIABLES["WERCKER_GIT_COMMIT"] = "run_unittest_commit_hash"
      run_di = get_di(required_fields, ENV_VARIABLES, PREFIX, [mock_pipeline_step])
      return run( **run_di )

    def we_get_a_False_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(False)

