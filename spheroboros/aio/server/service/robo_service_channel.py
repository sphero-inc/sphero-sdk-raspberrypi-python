#!/usr/bin/env python3


class RoboServiceChannel:
    '''A Channel is a generic class used for interfacing with the
    Sphero Communication Protocol
    '''
    def __init__(self, max_count):
        self.__used = []
        self.__instances = {}
        self.__available = list(range(1, max_count))

    @property
    def used(self):
        return self.__used

    @property
    def instances(self):
        return self.__instances

    def register(self, instance=None):
        try:
            channel_id = self.__available.pop()
            self.__instances[channel_id] = instance
            self.__used.append(channel_id)
            return channel_id
        except IndexError:
            return 0

    def unregister(self, channel_id):
        try:
            self.__used.remove(channel_id)
            self.__instances.pop(channel_id)
            self.__available.append(channel_id)
        except:
            raise
