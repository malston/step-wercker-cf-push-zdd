from config import Config
from pipeline_step_base import PipelineStepInterface

class StopStringFactory(PipelineStepInterface):
  def __init__(self, appname):
    self.appname = appname
    self.cfg = Config()
    self.env = {}

  def _get_helper(self, var_name):
    return self.env.get(self.cfg.make_name(var_name))

  def generate_stop_string(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    app_name = self.app_name()
    cmd = kwargs.get(self.cfg.CF_CMD)
    stopString = "{0} stop {1}".format(cmd, app_name)
    return stopString

  def run(self, **kwargs):
    err = False
    return (self.generate_stop_string(**kwargs), err)
  
  def app_name(self):
    return self.appname

def stop_app_string(**kwargs):
  return StopStringFactory().run(**kwargs)
