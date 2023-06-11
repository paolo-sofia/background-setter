from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class ImagesList:
    horizontal: List[str] = field(default_factory=list)
    vertical: List[str] = field(default_factory=list)

    @property
    def __dict__(self):
        """
        This function returns a dictionary representation of an object using the asdict() function.
        :return: The `__dict__` method is returning the dictionary representation of the object using the `asdict`
        function of the dataclasses package.
        """
        return asdict(self)
