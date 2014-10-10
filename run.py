from pipeline import execute
from config import Config
from make_push_string import PushStringFactory
from required_field_check import required_field_check

def run(**kwargs):
  return execute(**kwargs)

if __name__ == '__main__':
  pipeline = [
    required_field_check,
    PushStringFactory().run
  ]
  cfg = Config()
  dependencies = cfg.main_dependencies(pipeline)
  msg, err = run( **dependencies )
  exit_code = 0

  if err:
    exit_code = 1
  
  print(msg)
  exit(exit_code)

