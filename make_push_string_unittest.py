from pyvows import Vows, expect
from make_push_string import make_push_string
import os
from config import Config

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)

@Vows.batch
class ModuleTestsForRequiredFieldCheck(Vows.Context):
  def topic(self):
    rval = []
    rval.append(cfg.make_name("USE_MANIFEST"))
    rval.append(cfg.make_name("SPACE"))
    return rval

  class WhenExecutingWithNoRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name("USE_MANIFEST")] = "true"
      ENV_VARIABLES[cfg.make_name("APP_NAME")] = "my_test_app"
      ENV_VARIABLES["WERCKER_GIT_COMMIT"] = "ef306b2479a7ecd433 7875b4d954a4c8fc18 e237"
      ENV_VARIABLES[cfg.make_name("SPACE")] = "some-space"
      return make_push_string(required_fields=required_fields, 
                              env_variables=ENV_VARIABLES,
                              variable_prefix=PREFIX)

    def we_get_a_False_error_value(self, topic):
      push_string, err = topic
      expect(err).to_equal(False)

