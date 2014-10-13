from config import Config
from pipeline_step_base import PipelineStepInterface

class LoginStringFactory(PipelineStepInterface):
  def __init__(self):
    self.cfg = Config()
    self.env = {}

  def _get_helper(self, var_name):
    return self.env.get(self.cfg.make_name(var_name))

  def generate_login_string(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    org = self._get_helper(self.cfg.ORG)
    space = self._get_helper(self.cfg.SPACE)
    usr_pass = self._get_helper(self.cfg.USER_PASS)
    usr_name = self._get_helper(self.cfg.USER_NAME)
    cmd = kwargs.get(self.cfg.CF_CMD)
    return "{0} login -u {1} -p {2} -o {3} -s {4}".format(cmd, usr_name, usr_pass, org, space)

  def run(self, **kwargs):
    err = False
    return (self.generate_login_string(**kwargs), err)
  
