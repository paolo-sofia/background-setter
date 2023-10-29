import pathlib
from typing import List

from screen.screen import Screen
from window_protocol.x11 import X11
import subprocess


class Wayland(X11):
    HYPRPAPER_CONFIG_PATH: str = "~/.config/hypr/hyprpaper.conf"

    def update_wayland_background(self, image_path: pathlib.Path) -> None:
        """
        This function updates the KDE desktop background by modifying a configuration file with a new image path.

        :param image_path: The path to the image file that will be set as the KDE desktop background
        :type image_path: str
        :return: nothing (`None`).
        """
        subprocess.Popen(["swaybg", "-i", str(image_path)])
        subprocess.Popen(["eww", "reload"])
        return

    # @staticmethod
    # def get_screens() -> List[Screen]:
    #     pass
    #
    # def update_background_image(self, image_path: pathlib.Path) -> None:
    #     pass
    #
    # def update_gnome_background(self, image_path: pathlib.Path) -> None:
    #     pass
    #
    # def update_kde_background(self, image_path: pathlib.Path) -> None:
    #     pass
