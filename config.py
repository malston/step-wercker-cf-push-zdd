import subprocess
import os
import string
import random

class Config():
  RANDOM_HASH = None

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
    self.RANDOM_ROUTE = "" #"--random-route"
    self.CONST = {}
    self.CONST[self.PREFIX] = "WERCKER_CF_PUSH_ZDD"
    self.CONST[self.REQUIRED] = []
    self.CONST[self.REQUIRED].append(self.MANIFEST)
    self.CONST[self.REQUIRED].append(self.SPACE)
    self.CONST[self.REQUIRED].append(self.ORG)
    self.CONST[self.REQUIRED].append(self.USER_PASS)
    self.CONST[self.REQUIRED].append(self.USER_NAME)
    self.CONST[self.REQUIRED].append(self.APP_NAME)
    self.CONST[self.REQUIRED].append(self.API_URL)
    self.CONST[self.REQUIRED].append(self.DOMAIN)
    self.CONST[self.REQUIRED].append(self.HOST)
  
  def get(self, key):
    return self.CONST.get(key)

  def make_name(self, base):
    return "{0}_{1}".format(self.get(self.PREFIX), base)

  def get_app_name(self, env):
    app_var_name = self.make_name(self.APP_NAME)
    app_name = env.get(app_var_name)
    random_hash = self._get_hash(env)
    new_app_name = "{0}_{1}".format(app_name, random_hash)
    return (app_var_name, new_app_name, app_name)

  def set_app_name(self, env):
    app_var_name, new_app_name, _ = self.get_app_name(env)
    env[app_var_name] = new_app_name

  def get_host_name(self, env):
    host_var_name = self.make_name(self.HOST)
    host_name = env.get(host_var_name, "")
    return (host_var_name, host_name)
    
  def set_host_name(self, env):
    host_var_name, host_name = self.get_host_name(env)
    env[host_var_name] = host_name
  
  def get_domain_name(self, env):
    domain_var_name = self.make_name(self.DOMAIN)
    domain_name = env.get(domain_var_name, "")
    return domain_name
   
  def _get_hash(self, env):

    if not self.COMMIT_HASH in env:
      env[self.COMMIT_HASH] = self._id_generator()
    
    return env.get(self.COMMIT_HASH)


  def _id_generator(self, size=16, chars=string.ascii_uppercase + string.digits):
    random_hash = self.RANDOM_HASH

    if random_hash == None:
      random_hash = ''.join(random.choice(chars) for _ in range(size))
      self.RANDOM_HASH = random_hash

    return random_hash

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
    rfc_di[self.CF_CMD] = os.getenv("CF_CLI", "cf")
    return rfc_di

