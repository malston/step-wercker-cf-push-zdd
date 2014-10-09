from pyvows import Vows, expect
from required_field_check import required_field_check
import os
from config import Config

cfg = Config()
PREFIX=cfg.get(cfg.PREFIX)

def get_di(required_fields, env_vars, pfx):
  rfc_di = {}
  rfc_di[cfg.REQUIRED_FIELDS] = required_fields
  rfc_di[cfg.ENV_VARIABLES] = env_vars
  rfc_di[cfg.VARIABLE_PREFIX] = pfx
  rfc_di[cfg.CF_CMD] = "./cf"
  return rfc_di

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
      rfc_di = get_di(required_fields, ENV_VARIABLES, PREFIX)
      return required_field_check( **rfc_di )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingWithSomeRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      rfc_di = get_di(required_fields, ENV_VARIABLES, PREFIX)
      return required_field_check( **rfc_di )

    def we_get_a_True_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(True)

  class WhenExecutingWithAllRequiredFields(Vows.Context):    
    def topic(self, required_fields):
      ENV_VARIABLES = {}
      ENV_VARIABLES[cfg.make_name(cfg.MANIFEST)] = "true"
      ENV_VARIABLES[cfg.make_name(cfg.SPACE)] = "some-space"
      rfc_di = get_di(required_fields, ENV_VARIABLES, PREFIX)
      return required_field_check( **rfc_di )

    def we_get_a_False_error_value(self, topic):
      msg, err = topic
      expect(err).to_equal(False)

