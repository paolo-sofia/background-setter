from dataclasses import dataclass

from background_setter.screen.screen_offset import ScreenOffset
from background_setter.screen.screen_resolution import ScreenResolution
from screen_orientation import ScreenOrientation


@dataclass(slots=True)
class Screen:
    resolution: ScreenResolution
    offset: ScreenOffset
    orientation: ScreenOrientation = ScreenOrientation.HORIZONTAL

    def __post_init__(self) -> None:
        self.orientation = ScreenOrientation.VERTICAL if self.resolution.width > self.resolution.height \
            else ScreenOrientation.HORIZONTAL
        return
