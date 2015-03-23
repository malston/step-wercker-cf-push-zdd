from pipeline import execute
from config import Config
from make_push_string import PushStringFactory
from login_string import LoginStringFactory
from required_field_check import required_field_check
from route_detour import RouteDetourStringFactory
import os

def run(**kwargs):
  return execute(**kwargs)

if __name__ == '__main__':
  pipeline = [
    required_field_check,
    LoginStringFactory().run,
    PushStringFactory().run,
    RouteDetourStringFactory( action=RouteDetourStringFactory.ROUTE_MAP, 
                              route_definition=RouteDetourStringFactory.ROUTE_SMART_NAME ).run,
    RouteDetourStringFactory( action=RouteDetourStringFactory.ROUTE_UNMAP, 
                              route_definition=RouteDetourStringFactory.ROUTE_SMART_NAME ).run
  ]    
  cfg = Config()
  dependencies = cfg.main_dependencies(pipeline)
  msg, err = run( **dependencies )
  exit_code = 0

  if err:
    exit_code = 1
 
  if "DEBUG_STEP" in os.environ and os.environ["DEBUG_STEP"] == 'true':
    print(msg)

  exit(exit_code)

