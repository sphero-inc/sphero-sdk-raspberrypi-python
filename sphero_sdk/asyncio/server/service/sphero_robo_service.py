#!/usr/bin/env python3

from service.robo_service_base import RoboServiceBase
from service.robo_service_channel import RoboServiceChannel
from port.sphero_port_base import SpheroPortBase as PortBase
from parser.sphero_parser_base import SpheroParserBase as ParserBase
from handler.sphero_handler_base import SpheroHandlerBase as HandlerBase
from port.uart_sphero_port import UARTSpheroPort
from parser.api_sphero_parser import Parser
from handler.api_sphero_handler import Handler
import dbussy as dbus
from ravel import interface, INTERFACE, session_bus, method, ErrorReturn


bus_name = 'com.sphero.roboService'
interface_name = 'com.sphero.roboService'


@interface(INTERFACE.SERVER, name=interface_name)
class SpheroRoboService(RoboServiceBase):
    __MAXIMUM_NODE_COUNT = 16
    __MAXIMUM_PORT_COUNT = 16

    def __init__(self, loop, bus=session_bus(), path='/'):
        RoboServiceBase.__init__(self)
        self.loop = loop
        self.bus = bus
        self.path = path
        self.nodes = RoboServiceChannel(self.__MAXIMUM_NODE_COUNT)
        self.ports = RoboServiceChannel(self.__MAXIMUM_PORT_COUNT)
        self.bus.attach_asyncio(loop)
        self.bus.request_name(
            bus_name=bus_name,
            flags=dbus.DBUS.NAME_FLAG_DO_NOT_QUEUE
        )
        self.bus.register(path=path, fallback=True, interface=self)

        port = UARTSpheroPort(
                loop,
                None,
                Parser,
                Handler,
                '/dev/ttyS0'
        )
        port_id = self.ports.register(port)
        port.port_id = port_id


    @method(name='registerAsNode', in_signature='', out_signature='y')
    def register_as_node(self):
        try:
            node_id = self.nodes.register()
            return [node_id]
        except:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_LIMITS_EXCEEDED, 'Node Limit Reached')

    @method(name='unregisterNode', in_signature='y',
            arg_keys=['ID'], out_signature='')
    def unregister_node(self, ID):
        try:
            self.nodes.unregister(ID)
        except:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_FILE_NOT_FOUND, 'Node Does Not Exist')

    @method(name='registerPort', in_signature='a{ss}', out_signature='y')
    def register_port(self, portDict):
        try:
            port = PortBase.from_type_string(portDict['type'])(
                    ParserBase.from_type_string(portDict['protocol']),
                    HandlerBase.from_type_string(portDict['protocol'])
            )
            port_id = self.ports.register(port)
            port.port_id = port_id
        except IndexError:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_LIMITS_EXCEEDED, 'Port Limit Reached')
        except NotImplementedError:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_NOT_SUPPORTED, 'Not Implemented')
        else:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_SPAWN_SETUP_FAILED, 'Bad Configuration')

        return [port_id]

    @method(name='unregisterPort', in_signature='y',
            arg_keys=['ID'], out_signature='')
    def unregister_port(self, ID):
        try:
            self.ports.unregister(ID)
        except:
            raise ErrorReturn(
                    dbus.DBUS.ERROR_FILE_NOT_FOUND, 'Port Does Not Exist')

    @method(name='listRegisteredPorts', in_signature='', out_signature='s')
    def list_registered_ports(self):
        try:
            return [str(self.ports.used)]
        except:
            raise ErrorReturn(dbus.DBUS.ERROR_FAILED, 'DBUS Error Failed')
