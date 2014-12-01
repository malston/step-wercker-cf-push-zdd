from config import Config
import json

JSON_STRUCT = {
  "ENTITY": "entity",
  "RES": "resources",
  "SPACE_NAME": "name",
  "ROUTE_NAME": "host",
  "ORG_NAME": "name",
  "APP_NAME": "name",
  "SPACE_URL": "spaces_url",
  "ROUTE_URL": "routes_url",
  "APP_URL": "apps_url"
}

class AppInfo():
  cfg = Config()

  def __init__(self, **kwargs):
    self.cf_cli = kwargs.get(AppInfo.cfg.CF_CMD)
    self.env = kwargs.get(AppInfo.cfg.ENV_VARIABLES)
    self.sys_call = kwargs.get(AppInfo.cfg.SYS_CALL)
    self.org = self.env.get(AppInfo.cfg.make_name(AppInfo.cfg.ORG))
    self.space = self.env.get(AppInfo.cfg.make_name(AppInfo.cfg.SPACE))
    _, self.new_app_name, self.app_name = AppInfo.cfg.get_app_name(self.env)
    _, self.host_name = AppInfo.cfg.get_host_name(self.env)
  
  def _orgs_url(self):
    return "/v2/organizations"

  def _space_url_generator(self, json_string):
    org_object = self._url_generator(json_string, JSON_STRUCT["ORG_NAME"], self.org, self._default_compare )
    space_url = org_object[0][JSON_STRUCT["SPACE_URL"]]
    return space_url

  def _route_url_generator(self, json_string):
    space_object = self._url_generator(json_string, JSON_STRUCT["SPACE_NAME"], self.space, self._default_compare )
    route_url = space_object[0][JSON_STRUCT["ROUTE_URL"]]
    return route_url

  def _app_url_generator(self, json_string):
    route_object = self._url_generator(json_string, JSON_STRUCT["ROUTE_NAME"], self.host_name, self._default_compare )
    app_url = route_object[0][JSON_STRUCT["APP_URL"]]
    return app_url

  def _app_details(self, json_string):
    return self._url_generator(json_string, JSON_STRUCT["APP_NAME"], self.new_app_name, self._negative_compare )

  def _default_compare(self, l, r):
    return l == r

  def _negative_compare(self, l, r):
    return l != r

  def _url_generator(self, json_string, keyname, compare_value, compare_functor):
    jsonO = json.loads(json_string)
    url = [ x[JSON_STRUCT["ENTITY"]] for x in jsonO[JSON_STRUCT["RES"]] if compare_functor(x[JSON_STRUCT["ENTITY"]][keyname], compare_value)]
    return url

  def get_existing_app_details(self):
    spaceurl, org_err = self._get_entity(self._orgs_url(), self._space_url_generator)
    routeurl, space_err = self._get_entity(spaceurl, self._route_url_generator)
    appurl, route_err = self._get_entity(routeurl, self._app_url_generator)
    appdetails, app_err = self._get_entity(appurl, self._app_details)
    return (appdetails, [org_err, space_err, route_err, app_err])

  def _command_create(self, url):
    return "{1} curl {0} -X 'GET'".format(url, self.cf_cli )
 
  def _get_entity(self, url, response_parser):
    cmd = self._command_create(url)
    stdout, err = self.sys_call(cmd)

    if not err:
      response = response_parser(stdout)
    
    else:
      response = stdout

    return (response, err)

