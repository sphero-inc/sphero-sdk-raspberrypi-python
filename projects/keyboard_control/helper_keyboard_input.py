import sys
import termios
import tty


class KeyboardHelper:

    def __init__(self):
        self.__key_code = -1
        self.__loop = True
        self.__callback = None
        self.__original_settings = termios.tcgetattr(sys.stdin)

    @property
    def key_code(self):
        return self.__key_code

    @key_code.setter
    def key_code(self, value):
        self.__key_code = value

    def set_callback(self, callback):
        self.__callback = callback

    def get_key_continuous(self):
        """continuous_get_key records keystrokes in a while loop controlled by the private variable __loop.

        """
        while self.__loop:
            self.__get_key()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)

    def end_get_key_continuous(self):
        """end_loop sets the private variable __loop to false so that the while loop from continuous_get_key is stopped.

        """
        self.__loop = False

    def __get_key(self):
        tty.setcbreak(sys.stdin)
        key_code = ord(sys.stdin.read(1))
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)
        self.__callback(key_code)
