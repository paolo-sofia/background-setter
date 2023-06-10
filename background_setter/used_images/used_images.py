import datetime
import json
from dataclasses import dataclass, asdict

from background_setter.used_images.available_images import ImagesList


@dataclass
class UsedImages:
    images: ImagesList
    last_update: str = datetime.date.fromtimestamp(0).strftime('%Y-%m-%d')

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)
