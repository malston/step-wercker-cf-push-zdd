from config import Config

class AppInfo():
  cfg = Config()

  def __init__(self, **kwargs):
    self.env = kwargs.get(AppInfo.cfg.ENV_VARIABLES)
    self.sys_call = kwargs.get(AppInfo.cfg.SYS_CALL)
    self.org = self.env.get(AppInfo.cfg.make_name(AppInfo.cfg.ORG))
    self.space = self.env.get(AppInfo.cfg.make_name(AppInfo.cfg.SPACE))
    _, self.new_app_name, self.app_name = AppInfo.cfg.get_app_name(self.env)

  def _get_routing_table_for(self, route):
    # cf curl /v2/organizations -X 'GET'
    # match entity.name
    # entity.spaces_url
    # cf curl <spaces_url> -X 'GET'
    # match entity.name
    # entity.routes_url
    # match entity.host
    # entity.apps_url
    # match entity.name
    return []

  def _command_create(self, url):
    return "cf curl {0} -X 'GET'".format(url)
 
  def _get_entity(self, url, response_parser):
    cmd = self._command_create(url)
    stdout, err = self.sys_call(cmd)

    if not err:
      response = response_parser(stdout)

    return response

