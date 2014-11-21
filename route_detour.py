from config import Config
from pipeline_step_base import PipelineStepInterface

class RouteDetourStringFactory(PipelineStepInterface):
  ROUTE_FROM_HOST = 1
  ROUTE_FROM_NAME = 2
  ROUTE_SMART_NAME = 3
  ROUTE_MAP = "map-route"
  ROUTE_UNMAP = "unmap-route"

  def __init__(self, **setup):
    self.cf_action = setup.get("action")
    self.domain_name = self.route_from(setup.get("route_definition"))
    self.cfg = Config()
    self.env = {}
    self.sys_call = {}

  def route_from(self, route_definition):
    functor = self.smart_route

    if route_definition == self.ROUTE_FROM_HOST:
      functor = self.host_name

    elif route_definition == self.ROUTE_FROM_NAME:
      functor = self.app_name

    elif route_definition == self.ROUTE_SMART_NAME:
      functor = self.smart_route

    return functor

  def host_name(self):
    _, host_name = self.cfg.get_host_name(self.env)
    return host_name

  def app_name(self):
    _, _, app_name = self.cfg.get_app_name(self.env)
    return app_name

  def smart_route(self):
    route = self.host_name()
    
    if route == "":
      route = self.app_name()  

    return route

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

  def generate_routing_string(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    cmd = kwargs.get(self.cfg.CF_CMD)
    _, app_name, _ = self.cfg.get_app_name(self.env)
    return "{0} {1} {2} {3}".format(cmd, self.cf_action, app_name, self.domain_name())

  def run(self, **kwargs):
    err = False
    return (self.generate_routing_string(**kwargs), err)
  

