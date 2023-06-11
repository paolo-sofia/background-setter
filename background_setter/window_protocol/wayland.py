import pathlib
from typing import List

from background_setter.screen.screen import Screen
from background_setter.window_protocol.window_protocol import WindowProtocol


class Wayland(WindowProtocol):
    pass

    @staticmethod
    def get_screens() -> List[Screen]:
        pass

    def update_background_image(self, image_path: pathlib.Path) -> None:
        pass

    def update_gnome_background(self, image_path: pathlib.Path) -> None:
        pass

    def update_kde_background(self, image_path: pathlib.Path) -> None:
        pass
