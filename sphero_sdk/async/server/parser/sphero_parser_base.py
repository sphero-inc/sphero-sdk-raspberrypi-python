#!/usr/bin/env python3


class SpheroParserBase:
    """The base class for the parser."""
    __slots__ = ['_message_handler', '_error_handler']

    def __init__(self, message_handler, error_handler):
        """The base class for the parser.

        Args:
            message_handler (func): A function that takes a Message as input.
            error_handler (func): A function that takes a malformed message in the form of a bytearray as input.
        """
        self._message_handler = message_handler
        self._error_handler = error_handler

    def feed(self, data):
        """Feeds the Parser new raw byte data.

        Calls message_handler and error_handler.

        Raises:
            NotImplementedError: This function must be implemented by the class that inherits from SpheroParserBase.
        """
        raise NotImplementedError

    def set_message_handler(self, message_handler):
        """Sets this parser's message handler.

        Args:
            message_handler (func): A function that takes a Message as input.

        """
        self._message_handler = message_handler

    def set_error_handler(self, error_handler):
        """Sets this parser's error handler.

        Args:
            error_handler (func): A function that takes a malformed message in the form of a bytearray as input.

        """
        self._error_handler = error_handler

    @staticmethod
    def from_type_string(type_string):
        """
        Gives the parser class corresponding to the input type_string.

        Args:
            type_string (str): A string indicating the desired type of parser.
                Currently only 'api' and 'shell' types are supported, but 'shell' must be implemented by the inheriting
                class.

        Raises:
            NotImplementedError: Support for the 'shell' type is not currently implemented.
            AttributeError: Raised if the input type_string is not supported.

        Returns:
            The parser class corresponding to the input type_string.

        """
        if type_string == 'api':
            import parser.api_sphero_parser as api_sphero_parser
            return api_sphero_parser.Parser
        if type_string == 'shell':
            raise NotImplementedError
        else:
            raise AttributeError
