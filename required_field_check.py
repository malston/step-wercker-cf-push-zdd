def required_field_check(**kwargs):
  err = False
  msg = ""
  pfx = kwargs.get("variable_prefix")

  for fieldname in kwargs.get("required_fields"):
    fieldname = "{0}_{1}".format(pfx, fieldname)

    if not fieldname in kwargs.get("env_variables"):
      err = True
      msg = "Required ENV Variable not set: %s" % (fieldname)

  return (msg, err)
