from config import Config

def required_field_check(**kwargs):
  cfg = Config()
  err = False
  msg = ""

  for fieldname in kwargs.get(cfg.REQUIRED_FIELDS):
    fieldname = cfg.make_name(fieldname)

    if not fieldname in kwargs.get(cfg.ENV_VARIABLES):
      err = True
      msg += "Required ENV Variable not set: %s" % (fieldname)

  return (msg, err)
