from dataclasses import dataclass

from .screen_offset import ScreenOffset
from .screen_orientation import ScreenOrientation
from .screen_resolution import ScreenResolution


@dataclass
class Screen:
    resolution: ScreenResolution
    offset: ScreenOffset
    orientation: ScreenOrientation = ScreenOrientation.HORIZONTAL

    def __post_init__(self) -> None:
        """
        This function sets the orientation of the screen based on the resolution.
        :return: `None`.
        """
        self.orientation = ScreenOrientation.VERTICAL if self.resolution.width < self.resolution.height \
            else ScreenOrientation.HORIZONTAL
        return
