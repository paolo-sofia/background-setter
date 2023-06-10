import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict

from background_setter.screen.screen_orientation import ScreenOrientation


@dataclass
class ImagesList:
    horizontal: List[str] = field(default_factory=list)
    vertical: List[str] = field(default_factory=list)

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            ScreenOrientation.HORIZONTAL: self.horizontal,
            ScreenOrientation.VERTICAL: self.vertical
        }
