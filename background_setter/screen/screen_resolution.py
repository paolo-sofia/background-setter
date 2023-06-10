from dataclasses import dataclass
from numbers import Number


@dataclass
class ScreenResolution:
    width: int
    height: int

    @staticmethod
    def check_value(value: Number) -> int:
        """
        The function checks if the input value is an integer and returns it as an integer, otherwise it converts it to
        an integer and returns it.

        :param value: The parameter "value" is of type "Number", which means it can be either an integer or a float. The
        function "check_value" takes this parameter and returns an integer value. If the input value is already an
        integer, it is returned as is. Otherwise, it is converted to an integer and returned.
        :return: an integer value. If the input value is already an integer, it will be returned as is. If the input
        value is not an integer, it will be converted to an integer and then returned.
        """
        return value if isinstance(value, int) else int(value)

    def __post_init__(self) -> None:
        """
        The function initializes the width and height attributes of an object and checks if they are numbers, setting
        them to 0 if they are not.
        :return: `None`.
        """
        if not isinstance(self.width, Number):
            self.width = 0
        self.width = self.check_value(self.width)

        if not isinstance(self.height, Number):
            self.height = 0
        self.height = self.check_value(self.height)
        return
