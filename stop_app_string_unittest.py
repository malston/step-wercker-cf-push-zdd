from pyvows import Vows, expect
from stop_app_string import StopStringFactory
import os
from config import Config

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)
appname = "my_test_app"
cf_command = "cf"

@Vows.batch
class ModuleTestsForRequiredFieldCheck(Vows.Context):
  def topic(self):
    rval = []
    rval.append(cfg.make_name(cfg.MANIFEST))
    rval.append(cfg.make_name(cfg.SPACE))
    return rval

  class WhenExecutingWithNoRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.APP_NAME)] = appname
      stopString = StopStringFactory(appname)
      return stopString.run(required_fields=required_fields, 
                              env_variables=ENV_VARIABLES,
                              variable_prefix=PREFIX,
                              cf_cmd=cf_command)

    def we_get_a_False_error_value(self, topic):
      push_string, err = topic
      expect(err).to_equal(False)
      expect(push_string).to_equal("{0} stop {1}".format(cf_command, appname)
)


