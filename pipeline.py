from make_push_string import make_push_string
from config import Config
import copy

def execute(**kwargs):
  msg = "No Pipeline steps configured"
  err = True
  cfg = Config()
  sys_call = kwargs.get(cfg.SYS_CALL)
  pipeline = kwargs.get(cfg.PIPELINE, [])

  for step in pipeline:
    msg, err = step(**copy.deepcopy(kwargs))
    
    if err:
      break

    else:
      msg, err = sys_call(msg)

      if err:
        break
    
  return (msg, err)
