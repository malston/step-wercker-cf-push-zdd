import subprocess
import os
import string
import random

class Config():
  def __init__(self):
    self.COMMIT_HASH = "WERCKER_GIT_COMMIT"
    self.MANIFEST = "USE_MANIFEST"
    self.BUILDPACK = "BUILDPACK"
    self.COMMAND = "COMMAND"
    self.DOMAIN = "DOMAIN"
    self.INSTANCES = "NUM_INSTANCES"
    self.MEMORY = "MEMORY"
    self.HOST = "HOST"
    self.BASE_HOST = "BASE_HOST"
    self.PATH = "PATH"
    self.STACK = "STACK"
    self.NO_HOST = "NO_HOSTNAME"
    self.NO_ROUTE = "NO_ROUTE"
    self.NO_START = "NO_START"
    self.SPACE = "SPACE"
    self.ORG = "ORG"
    self.USER_PASS = "USER_PASS"
    self.USER_NAME = "USER_NAME"
    self.APP_NAME = "APP_NAME"
    self.API_URL = "API_URL"
    self.PREFIX = "prefix"
    self.REQUIRED = "required"
    self.REQUIRED_FIELDS = "required_fields"
    self.ENV_VARIABLES = "env_variables"
    self.VARIABLE_PREFIX = "variables_prefix"
    self.SYS_CALL = "system_call"
    self.PIPELINE = "pipeline"
    self.CF_CMD = "cf_cmd"
    self.RANDOM_ROUTE = "--random-route"
    self.CONST = {}
    self.CONST[self.PREFIX] = "WERCKER_CF_PUSH_CLOUDFOUNDRY"
    self.CONST[self.REQUIRED] = []
    self.CONST[self.REQUIRED].append(self.MANIFEST)
    self.CONST[self.REQUIRED].append(self.SPACE)
    self.CONST[self.REQUIRED].append(self.ORG)
    self.CONST[self.REQUIRED].append(self.USER_PASS)
    self.CONST[self.REQUIRED].append(self.USER_NAME)
    self.CONST[self.REQUIRED].append(self.APP_NAME)
    self.CONST[self.REQUIRED].append(self.API_URL)
  
  def get(self, key):
    return self.CONST.get(key)

  def make_name(self, base):
    return "{0}_{1}".format(self.get(self.PREFIX), base)

  def set_app_name(self, env):
    app_var_name = self.make_name(self.APP_NAME)
    app_name = env.get(app_var_name)
    random_hash = env.get(self.COMMIT_HASH, self._id_generator())
    app_name = "{0}_{1}".format(app_name, random_hash)
    env[app_var_name] = app_name

  def set_host_name(self, env):
    host_var_name = self.make_name(self.HOST)
    host_name = env.get(host_var_name, "")
    env[host_var_name] = host_name
    return (host_var_name, host_name)
   
  def _id_generator(self, size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

  def system_call(self, cmdString):
    stdout = ""
    err = False

    try:
      stdout = subprocess.check_output(cmdString, shell=True)
      
    except subprocess.CalledProcessError as e:
      stdout = "error: {0}".format(e)
      err = True

    return (stdout, err)

  def main_dependencies(self, pipeline):
    PREFIX = self.get(self.PREFIX)
    REQUIRED_FIELDS = self.get(self.REQUIRED)
    rfc_di = {}
    rfc_di[self.REQUIRED_FIELDS] = REQUIRED_FIELDS
    rfc_di[self.ENV_VARIABLES] = os.environ
    rfc_di[self.VARIABLE_PREFIX] = PREFIX
    rfc_di[self.SYS_CALL] = self.system_call
    rfc_di[self.PIPELINE] = pipeline
    rfc_di[self.CF_CMD] = "echo"
    return rfc_di

