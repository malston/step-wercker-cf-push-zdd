from config import Config

cfg = Config()
FIELD_FLAG_ACTIONS = {}
FIELD_FLAG_ACTIONS[cfg.make_name("USE_MANIFEST")] =   lambda v: "--no-manifest" if v == False else ""
FIELD_FLAG_ACTIONS[cfg.make_name("BUILDPACK")] =      lambda v: ("-b %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("COMMAND")] =        lambda v: ("-c %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("DOMAIN")] =         lambda v: ("-d %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("NUM_INSTANCES")] =  lambda v: ("-i %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("MEMORY")] =         lambda v: ("-m %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("HOST")] =           lambda v: ("-n %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("PATH")] =           lambda v: ("-p %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("STACK")] =          lambda v: ("-s %s" % v) if v != None else ""
FIELD_FLAG_ACTIONS[cfg.make_name("NO_HOSTNAME")] =    lambda v: "--no-hostname" if v != None and v == True else ""
FIELD_FLAG_ACTIONS[cfg.make_name("NO_ROUTE")] =       lambda v: "--no-route" if v != None and v == True else ""
FIELD_FLAG_ACTIONS[cfg.make_name("NO_START")] =       lambda v: "--no-start" if v != None and v == True else ""

def clean_append(current, extend):
  return "%s %s" % (current, extend)

def make_push_string(**kwargs):
  err = False
  push_string = ""
  push_string = clean_append(kwargs.get("cf_cmd"), "push")
  new_app_name = cfg.new_app_name(kwargs.get("env_variables"))

  if new_app_name == None:
    err = True

  push_string = clean_append(push_string, new_app_name)

  for flag_name, flag_lambda in FIELD_FLAG_ACTIONS.iteritems():
    flag_name = cfg.make_name("USE_MANIFEST")
    flag_value = kwargs.get("env_variables").get(flag_name)
    string_to_append = flag_lambda(flag_value)
    push_string = clean_append(push_string, string_to_append)

  return (push_string, err)
