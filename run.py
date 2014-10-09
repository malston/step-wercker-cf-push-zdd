import os
from required_field_check import required_field_check
from pipeline import execute
from config import Config

def run(**kwargs):
  msg, err = required_field_check(**kwargs)

  if err == False:
    push_string, err = execute(**kwargs)
    msg = push_string

  return (msg, err)

def mock_system_call(cmd_string):
  print("Running cmd: {0}".format(cmd_string))
  return (cmd_string, False)

def main_dependencies():
  cfg = Config()
  PREFIX = cfg.get(cfg.PREFIX)
  REQUIRED_FIELDS = cfg.get(cfg.REQUIRED)
  rfc_di = {}
  rfc_di[cfg.REQUIRED_FIELDS] = REQUIRED_FIELDS
  rfc_di[cfg.ENV_VARIABLES] = os.environ
  rfc_di[cfg.VARIABLE_PREFIX] = PREFIX
  rfc_di[cfg.SYS_CALL] = mock_system_call#cfg.system_call,
  rfc_di[cfg.CF_CMD] = "./cf"
  return rfc_di

if __name__ == '__main__':
  msg, err = run( **main_dependencies() )
  exit_code = 0

  if err:
    exit_code = 1
  
  print(msg)
  exit(exit_code)

