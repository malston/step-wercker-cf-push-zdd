from pyvows import Vows, expect
from run import run
import os
from config import Config

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)

@Vows.batch
class ModuleTestsForRun(Vows.Context):
  def topic(self):
    rval = []
    rval.append("USE_MANIFEST")
    rval.append("SPACE")
    return rval

  class WhenExecutingYieldsError(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      return run( required_fields=required_fields, 
                  env_variables=ENV_VARIABLES, 
                  variable_prefix=PREFIX )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingYieldsSuccess(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name("USE_MANIFEST")] = "true"
      ENV_VARIABLES[cfg.make_name("SPACE")] = "some-space"
      ENV_VARIABLES[cfg.make_name("APP_NAME")] = "my_test_app"
      ENV_VARIABLES["WERCKER_GIT_COMMIT"] = "ef306b2479a7ecd433 7875b4d954a4c8fc18 e237"
      return run( required_fields=required_fields, 
                  env_variables=ENV_VARIABLES, 
                  variable_prefix=PREFIX,
                  cf_cmd="./cf" )

    def we_get_a_False_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(False)

