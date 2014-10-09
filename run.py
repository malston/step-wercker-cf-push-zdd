import os
from required_field_check import required_field_check
from make_push_string import make_push_string
from config import Config

def run(**kwargs):
  msg, err = required_field_check(**kwargs)

  if err == False:
    push_string, err = make_push_string(**kwargs)
    msg = push_string

  return (msg, err)

if __name__ == '__main__':
  cfg = Config()
  PREFIX = cfg.get(cfg.PREFIX)
  REQUIRED_FIELDS = cfg.get(cfg.REQUIRED)
  msg, err = run( required_fields=REQUIRED_FIELDS, 
                  env_variables=os.environ,
                  variable_prefix=PREFIX,
                  cf_cmd="./cf" )

  exit_code = 0

  if err:
    exit_code = 1
  
  print(msg)
  exit(exit_code)

