from config import Config
from pipeline_step_base import PipelineStepInterface

class PushStringFactory(PipelineStepInterface):
  cfg = Config()
  FIELD_FLAG_ACTIONS = {}
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.MANIFEST)] =       lambda v: "--no-manifest" if v.lower() == 'false' else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.BUILDPACK)] =      lambda v: ("-b %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.COMMAND)] =        lambda v: ("-c %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.DOMAIN)] =         lambda v: ("-d %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.INSTANCES)] =      lambda v: ("-i %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.MEMORY)] =         lambda v: ("-m %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.HOST)] =           lambda v: PushStringFactory.cfg.RANDOM_ROUTE
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.PATH)] =           lambda v: ("-p %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.STACK)] =          lambda v: ("-s %s" % v) if v != "" else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_HOST)] =        lambda v: "--no-hostname" if v.lower() == 'true' else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_ROUTE)] =       lambda v: "--no-route" if v.lower() == 'true' else ""
  FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_START)] =       lambda v: "--no-start" if v.lower() == 'true' else ""

  def __init__(self):
    self.env = {}

  @staticmethod
  def clean_append(current, extend):
    return_value = current
    
    if extend.strip() != "":
      return_value = "%s %s" % (current, extend)

    return return_value

  def _stage_env_variables(self):
    self.cfg.set_host_name(self.env)
    self.cfg.set_app_name(self.env)

  def _get_values(self, **kwargs):
    cf_command_string = kwargs.get(self.cfg.CF_CMD)
    cf_action = "push"
    app_name = self.env.get(self.cfg.make_name(self.cfg.APP_NAME))
    return (cf_command_string, cf_action, app_name)

  def run(self, **kwargs):
    err = False
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    self._stage_env_variables()
    cf_command_string, cf_action, app_name = self._get_values(**kwargs)
    push_string = self.clean_append(cf_command_string, cf_action)
    push_string = self.clean_append(push_string, app_name)

    for flag_name, flag_lambda in self.FIELD_FLAG_ACTIONS.iteritems():
      flag_value = self.env.get(flag_name, "")
      string_to_append = flag_lambda(flag_value)
      push_string = self.clean_append(push_string, string_to_append)

    return (push_string, err)

def make_push_string(**kwargs):
  return PushStringFactory().run(**kwargs)
