from spherorvr.observer.observer_base import Observer
from spherorvr.observer.dal.rvr_dal import RvrDal
from spherorvr.observer.dal.rvr_parser import RvrParser
from spherorvr.observer.dal.rvr_port import RvrSerialPort
from spherorvr.observer.events.rvr_event_dispatcher import RvrEventDispatcher
from spherorvr.observer.commands import system_info
from spherorvr.observer.commands import drive


class SpheroRvr(Observer):

    def __init__(self):
        Observer.__init__(self)
        dispatcher = RvrEventDispatcher()
        parser = RvrParser(dispatcher)
        port = RvrSerialPort(parser)
        self._dal = RvrDal(port)

    def get_main_application_version(self, target, callback, timeout=None):
        did,\
        cid,\
        outputs = system_info.get_main_application_version()
        self._register_callback(did, cid, callback, outputs)
        self._dal.send_command(did, cid, target=target, timeout=timeout, outputs=outputs)
    
    def raw_motors(self, left_mode, left_speed, right_mode, right_speed, timeout=None):
        did,\
        cid,\
        inputs = drive.raw_motors(left_mode, left_speed, right_mode, right_speed)
        self._dal.send_command(did, cid, target=2, timeout=timeout, inputs=inputs)

    def reset_yaw(self, timeout=None):
        did,\
        cid = system_info.get_main_application_version()
        self._dal.send_command(did, cid, target=2, timeout=timeout)

    def drive_with_heading(self, speed, heading, flags, timeout=None):
        did,\
        cid,\
        inputs = drive.drive_with_heading(speed, heading, flags)
        self._dal.send_command(did, cid, target=2, timeout=timeout, inputs=inputs)

