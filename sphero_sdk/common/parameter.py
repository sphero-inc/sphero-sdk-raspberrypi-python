#! /usr/bin/env python3


class Parameter:
    __slots__ = ['__name', '__data_type', '__index', '__size', '__value']

    def __init__(self, *, name, data_type, index, size, value=None):
        self.__name = name
        self.__data_type = data_type
        self.__index = index
        self.__size = size
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def data_type(self):
        return self.__data_type

    @property
    def index(self):
        return self.__index

    @property
    def size(self):
        return self.__size

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
