#!/usr/bin/env python3

from service.robo_service_base import RoboServiceBase
from service.robo_service_channel import RoboServiceChannel


class Service(RoboServiceBase):
    __MAXIMUM_NODE_COUNT = 16
    __MAXIMUM_PORT_COUNT = 16

    def __init__(self):
        RoboServiceBase.__init__(self)        
        self.nodes = RoboServiceChannel(self.__MAXIMUM_NODE_COUNT)
        self.ports = RoboServiceChannel(self.__MAXIMUM_PORT_COUNT)
    
    def register_as_node(self):
        node_id = self.nodes.register()
        return node_id

    def unregister_node(self, ID):
        self.nodes.unregister(ID)

    def register_port(self, portDict):
        pass

    def unregister_port(self, ID):
        self.ports.unregister(ID)

    def list_registered_ports(self):
        return [str(self.ports.used)]
