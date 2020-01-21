import os
import sys
from util import make_response, run_handler


def get_runtime_env(event, body):
  '''
    Handler to dump lambda environment (For debug, etc.)
  '''
  path = os.popen("echo $PATH").read()
  directories = os.popen("find /opt -type d -maxdepth 4").read().split("\n")
  return make_response({
      'path': path,
      'syspath': sys.path,
      'directories': directories,
      'event': event
  })


def handler(event, context):
  return run_handler(get_runtime_env, event)
