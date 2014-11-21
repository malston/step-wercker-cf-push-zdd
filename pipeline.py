from make_push_string import make_push_string
from config import Config
import copy

def execute(**kwargs):
  msgList = []
  response_msg = "No Pipeline steps configured"
  err = True
  cfg = Config()
  sys_call = kwargs.get(cfg.SYS_CALL)
  pipeline = kwargs.get(cfg.PIPELINE, [])

  for step in pipeline:
    cmd, err = step(**copy.deepcopy(kwargs))
    
    if err:
      break

    else:
      msg, err = sys_call(cmd)

      if err:
        break
 
    msgList.append((cmd, msg))
    
  if len(msgList) == 0:
    msgList.append(response_msg)

  return (msgList, err)
