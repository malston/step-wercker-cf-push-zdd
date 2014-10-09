class Config():
  def __init__(self):
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
    self.CF_CMD = "cf_cmd"
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

  def set_new_host_name(self, env):
    app_var_name, app_name = self._app_name(env)
    host_var_name, host_name = self._host_name(env)
    self._set_base_host_name(env, host_name)
    self._set_host_name(env, host_name)
  
  def _set_host_name(self, env, host_name):
    host_var_name, _ = self._host_name(env)
    commit_hash = env.get("WERCKER_GIT_COMMIT")
    env[host_var_name] = "{0}-zdd-{1}".format(host_name, commit_hash)

  def _set_base_host_name(self, env, host_name):
    env[self.make_name(self.BASE_HOST)] = host_name

  def _app_name(self, env):
    app_var_name = self.make_name(self.APP_NAME)
    app_name = env.get(app_var_name)
    return (app_var_name, app_name)

  def _host_name(self, env):
    _, app_name = self._app_name(env)
    host_var_name = self.make_name(self.HOST)
    host_name = env.get(host_var_name, app_name)
    return (host_var_name, host_name)
    
