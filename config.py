class Config():
  def __init__(self):
    self.PREFIX="prefix"
    self.REQUIRED="required"
    self.CONST = {
      "prefix": "WERCKER_CF_PUSH_CLOUDFOUNDRY",
      "required": [
        "USE_MANIFEST",
        "SPACE",
        "ORG",
        "USER_PASS",
        "USER_NAME",
        "APP_NAME",
        "API_URL"
      ]
    }

  def get(self, key):
    return self.CONST.get(key)

  def make_name(self, base):
    return "{0}_{1}".format(self.get(self.PREFIX), base)

  def new_app_name(self, env):
    varname = self.make_name("APP_NAME")
    appname = env.get(varname)
    commit_hash = env.get("WERCKER_GIT_COMMIT")
    return "{0}-zdd-{1}".format(appname, commit_hash)
