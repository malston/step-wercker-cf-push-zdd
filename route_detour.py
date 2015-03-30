from config import Config
from pipeline_step_base import PipelineStepInterface
from app_info import AppInfo
from stop_app_string import StopStringFactory

class RouteDetourStringFactory(PipelineStepInterface):
  ROUTE_FROM_HOST = 1
  ROUTE_FROM_NAME = 2
  ROUTE_SMART_NAME = 3
  ROUTE_MAP = "map-route"
  ROUTE_UNMAP = "unmap-route"

  def __init__(self, **setup):
    self.cf_action = setup.get("action")
    self.host = self.route_from(setup.get("route_definition"))
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
    _, hostname = self.cfg.get_host_name(self.env)
    return hostname

  def app_name(self):
    _, _, app_name = self.cfg.get_app_name(self.env)
    return app_name

  def smart_route(self):
    route = self.host_name()
    
    if route == "":
      route = self.app_name()  

    return route

  def _string_formatter(self, cmd, action, name, domain, hostname):
    return "{0} {1} {2} {3} -n {4}; ".format(cmd, action, name, domain, hostname)

  def _unmap_route_stringgen(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    domain_name = self.cfg.get_domain_name(self.env)
    app_info = AppInfo( **kwargs )
    cmd = kwargs.get(self.cfg.CF_CMD)
    command_string = ""

    try:
      app_detail_list, _ = app_info.get_existing_app_details()

      for app in app_detail_list:
        command_string += self._string_formatter(cmd, self.cf_action, app["name"], domain_name, self.host())

    except:  
      command_string = "{0} routes".format(cmd)
       
    return command_string

  def _stop_app_string(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    domain_name = self.cfg.get_domain_name(self.env)
    app_info = AppInfo( **kwargs )
    cmd = kwargs.get(self.cfg.CF_CMD)
    command_string = ""

    try:
      app_detail_list, _ = app_info.get_existing_app_details()

      for app in app_detail_list:
        stopString = StopStringFactory(app["name"])
        cs, _ = stopString.run(**kwargs)
        command_string += cs+";"

    except:  
      command_string = "app can not be stopped"

    return command_string

  def generate_routing_string(self, **kwargs):
    self.env = kwargs.get(self.cfg.ENV_VARIABLES)
    domain_name = self.cfg.get_domain_name(self.env)
    cmd = kwargs.get(self.cfg.CF_CMD)
    command_string = ""
    
    if self.cf_action == self.ROUTE_UNMAP:
      command_string = self._unmap_route_stringgen(**kwargs)
      command_string += self._stop_app_string(**kwargs)
      
    else:
      _, app_name, _ = self.cfg.get_app_name(self.env)
      command_string = self._string_formatter(cmd, self.cf_action, app_name, domain_name, self.host())

    return command_string

  def run(self, **kwargs):
    err = False
    return (self.generate_routing_string(**kwargs), err)
  

