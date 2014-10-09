from make_push_string import make_push_string
from config import Config

def execute(**kwargs):
  msg = ""
  cfg = Config()
  push_string, err = make_push_string(**kwargs)
  
  if not err:
    sys_call = kwargs.get(cfg.SYS_CALL)
    msg, err = sys_call(push_string)

  return (msg, err)
