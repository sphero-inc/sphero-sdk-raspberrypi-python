class SensorStreamAttribute:

    __slots__ = ['__name', '__min_value', '__max_value', '__number_type']

    def __init__(self, name, min_value, max_value):
        self.__name = name
        self.__min_value = min_value
        self.__max_value = max_value

        # Determine if this attribute is a float or int
        test_value = self.__min_value + self.__max_value
        self.__number_type = int if isinstance(test_value, int) else float

    @property
    def name(self):
        return self.__name

    @property
    def minimum_value(self):
        return self.__min_value

    @property
    def maximum_value(self):
        return self.__max_value

    @property
    def number_type(self):
        return self.__number_type
