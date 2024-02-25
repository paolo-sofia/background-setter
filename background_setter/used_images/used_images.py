import datetime
from dataclasses import dataclass, asdict

from used_images.available_images import ImagesList


@dataclass
class UsedImages:
    images: ImagesList
    last_update: str = datetime.date.fromtimestamp(0).strftime('%Y-%m-%d')

    @property
    def __dict__(self):
        """
        This function returns a dictionary representation of an object using the asdict() function.
        :return: The `__dict__` method is returning the dictionary representation of the object using the `asdict`
        function of the dataclasses package.
        """
        return asdict(self)
