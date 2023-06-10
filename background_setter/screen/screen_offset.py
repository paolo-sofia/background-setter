from dataclasses import dataclass
from numbers import Number


@dataclass
class ScreenOffset:
    x: int
    y: int

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
        if not isinstance(self.x, Number):
            self.x = 0
        self.x = self.check_value(self.x)

        if not isinstance(self.y, Number):
            self.y = 0
        self.y = self.check_value(self.y)
        return
