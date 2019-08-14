import sys
import termios
import tty


class KeyboardHelper:

    def __init__(self):
        self.__key_code = -1
        self.__loop = True
        return

    @property
    def key_code(self):
        return self.__key_code

    @key_code.setter
    def key_code(self, value):
        self.__key_code = value
        return

    def get_key_continuous(self):
        """continuous_get_key records keystrokes in a while loop controlled by the private variable __loop.

        """
        while self.__loop:
            self.__get_key()
        return

    def end_get_key_continuous(self):
        """end_loop sets the private variable __loop to false so that the while loop from continuous_get_key is stopped.

        """
        self.__loop = False
        return

    def __get_key(self):
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)
        self.__key_code = ord(sys.stdin.read(1))
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        return self.__key_code
