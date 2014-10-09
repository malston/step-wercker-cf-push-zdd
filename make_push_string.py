from config import Config

cfg = Config()
FIELD_FLAG_ACTIONS = {}
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.MANIFEST)] =       lambda v: "--no-manifest" if v.lower() == 'false' else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.BUILDPACK)] =      lambda v: ("-b %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.COMMAND)] =        lambda v: ("-c %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.DOMAIN)] =         lambda v: ("-d %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.INSTANCES)] =      lambda v: ("-i %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.MEMORY)] =         lambda v: ("-m %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.HOST)] =           lambda v: ("-n %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.PATH)] =           lambda v: ("-p %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.STACK)] =          lambda v: ("-s %s" % v) if v != "" else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_HOST)] =        lambda v: "--no-hostname" if v != "" and v == True else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_ROUTE)] =       lambda v: "--no-route" if v != "" and v == True else ""
FIELD_FLAG_ACTIONS[cfg.make_name(cfg.NO_START)] =       lambda v: "--no-start" if v != "" and v == True else ""

def clean_append(current, extend):
  return_value = current
  
  if extend.strip() != "":
    return_value = "%s %s" % (current, extend)

  return return_value

def make_push_string(**kwargs):
  env = kwargs.get(cfg.ENV_VARIABLES)
  err = False
  cf_action = "push"
  push_string = clean_append(kwargs.get(cfg.CF_CMD), cf_action)
  app_name = env.get(cfg.make_name(cfg.APP_NAME))
  cfg.set_new_host_name(env)
  push_string = clean_append(push_string, app_name)

  for flag_name, flag_lambda in FIELD_FLAG_ACTIONS.iteritems():
    flag_value = env.get(flag_name, "")
    string_to_append = flag_lambda(flag_value)
    push_string = clean_append(push_string, string_to_append)

  return (push_string, err)
