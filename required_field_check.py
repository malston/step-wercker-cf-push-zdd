from config import Config

def required_field_check(**kwargs):
  cfg = Config()
  err = False
  msg = ""

  for fieldname in kwargs.get("required_fields"):
    fieldname = cfg.make_name(fieldname)

    if not fieldname in kwargs.get("env_variables"):
      err = True
      msg = "Required ENV Variable not set: %s" % (fieldname)

  return (msg, err)
