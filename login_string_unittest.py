from pyvows import Vows, expect
from login_string import LoginStringFactory
import os
from config import Config

cfg = Config()
PREFIX = cfg.get(cfg.PREFIX)
name = "myname"
space = "myspace"
passw = "mypass"
org = "myorg"

@Vows.batch
class ModuleTestsForLoginStringFactory(Vows.Context):
  def topic(self):
    env = {}   
    env[cfg.make_name(cfg.ORG)] = org
    env[cfg.make_name(cfg.SPACE)] = space
    env[cfg.make_name(cfg.USER_PASS)] = passw
    env[cfg.make_name(cfg.USER_NAME)] = name
    return env

  class WhenExecutingRunSuccessfully(Vows.Context):
    def topic(self, ENV_VARIABLES):
      return LoginStringFactory().run(env_variables=ENV_VARIABLES)

    def we_get_a_False_error_value(self, topic):
      push_string, err = topic
      expect(err).to_equal(False)

    def we_get_a_string_containing_name(self, topic):
      push_string, _ = topic
      expect((name in push_string)).to_equal(True)

    def we_get_a_string_containing_space(self, topic):
      push_string, _ = topic
      expect((space in push_string)).to_equal(True)

    def we_get_a_string_containing_password(self, topic):
      push_string, _ = topic
      expect((passw in push_string)).to_equal(True)

    def we_get_a_string_containing_org(self, topic):
      push_string, _ = topic
      expect((org in push_string)).to_equal(True)

