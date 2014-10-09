class Config():
  def __init__(self):
    self.MANIFEST = "USE_MANIFEST"
    self.BUILDPACK = "BUILDPACK"
    self.COMMAND = "COMMAND"
    self.DOMAIN = "DOMAIN"
    self.INSTANCES = "NUM_INSTANCES"
    self.MEMORY = "MEMORY"
    self.HOST = "HOST"
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

  def new_app_name(self, env):
    varname = self.make_name(self.APP_NAME)
    appname = env.get(varname)
    commit_hash = env.get("WERCKER_GIT_COMMIT")
    return "{0}-zdd-{1}".format(appname, commit_hash)
