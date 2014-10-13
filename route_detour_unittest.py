from pyvows import Vows, expect
from route_detour import RouteDetourStringFactory
import os
from config import Config

cfg = Config()

@Vows.batch
class ModuleTestsForRouteDetourStringFactory(Vows.Context):
  def topic(self):
    env = {}   
    return env

  class WhenExecutingRunSuccessfully(Vows.Context):
    def topic(self, ENV_VARIABLES):
      return RouteDetourStringFactory(action=RouteDetourStringFactory.ROUTE_MAP, 
                                      route_definition=RouteDetourStringFactory.ROUTE_FROM_HOST)
    
    class WhenRunningRouteDetourString(Vows.Context):
      ROUTE_DETOUR_CONTROL = {}

      def topic(self, RouteDetour, ENV_VARIABLES):
        self.ROUTE_DETOUR_CONTROL = RouteDetour
        return RouteDetour.run(env_variables=ENV_VARIABLES)

      def we_get_a_False_error_value(self, topic):
        push_string, err = topic
        expect(err).to_equal(False)

      def we_should_see_proper_action_in_command_string(self, topic):
        push_string, err = topic
        expect( (RouteDetourStringFactory.ROUTE_MAP in push_string) ).to_equal(True)

      def we_should_see_route_in_command_string(self, topic):
        push_string, err = topic
        route_name = self.ROUTE_DETOUR_CONTROL.domain_name()
        expect( (route_name in push_string) ).to_equal(True)

      def we_should_see_appname_in_command_string(self, topic):
        push_string, err = topic
        _, app_name, _ = cfg.get_app_name(self.ROUTE_DETOUR_CONTROL.env)
        expect( (app_name in push_string) ).to_equal(True)

