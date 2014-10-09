from pyvows import Vows, expect
from required_field_check import required_field_check
import os
from config import Config

cfg = Config()
PREFIX=cfg.get(cfg.PREFIX)

@Vows.batch
class ModuleTestsForRequiredFieldCheck(Vows.Context):
  def topic(self):
    rval = []
    rval.append(cfg.MANIFEST)
    rval.append(cfg.SPACE)
    return rval

  class WhenExecutingWithNoRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      return required_field_check( required_fields=required_fields, 
                                   env_variables=ENV_VARIABLES,
                                   variable_prefix=PREFIX
                                  )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingWithSomeRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      return required_field_check( required_fields=required_fields, 
                                   env_variables=ENV_VARIABLES,
                                   variable_prefix=PREFIX
                                  )
    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingWithAllRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      ENV_VARIABLES[cfg.make_name(cfg.SPACE)] = "some-space"
      return required_field_check( required_fields=required_fields, 
                                   env_variables=ENV_VARIABLES,
                                   variable_prefix=PREFIX
                                  )

    def we_get_a_False_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(False)

