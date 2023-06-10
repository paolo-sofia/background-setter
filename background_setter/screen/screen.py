from dataclasses import dataclass

from screen_orientation import ScreenOrientation


@dataclass(slots=True)
class Screen:
    width: int
    height: int
    x_offset: int
    y_offset: int
    orientation: str = None

    def __post_init__(self) -> None:
        self.orientation = ScreenOrientation.VERTICAL if self.width > self.height else ScreenOrientation.HORIZONTAL
