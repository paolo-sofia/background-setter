import logging
import pathlib
import re
import subprocess
from abc import ABC, abstractmethod
from typing import List, Iterator

from background_setter.screen.screen import Screen
from background_setter.screen.screen_resolution import ScreenResolution
from background_setter.window_protocol.desktop_environment import DesktopEnvironment


class WindowProtocol(ABC):
    """
    The `WindowProtocol` class is an abstract base class that provides methods for detecting the current desktop
    environment, retrieving the current screen resolution, and updating the background image.
    """

    def __init__(self, desktop_environment: DesktopEnvironment):
        self.desktop_environment: DesktopEnvironment = desktop_environment

    @staticmethod
    def get_desktop_resolution() -> ScreenResolution:
        """
        The function retrieves the current screen resolution of the desktop using the xrandr command in Python.
        :return: The function `get_desktop_resolution()` returns an instance of the `ScreenResolution` class, which
        represents the current screen resolution of the desktop. If the screen resolution cannot be determined, it
        returns a `ScreenResolution` instance with width and height set to 0.
        """
        output: Iterator[bytes] = iter(
            subprocess.Popen(['xrandr | grep current'], stdout=subprocess.PIPE, shell=True).stdout)
        for row in output:
            if screen_res := re.search(r'current \d+ x \d+', row.decode('UTF-8')):
                screen_res = [int(x) for x in re.findall(r'\d+', screen_res.group())]
                return ScreenResolution(*screen_res)
        return ScreenResolution(0, 0)

    @staticmethod
    @abstractmethod
    def get_screens() -> List[Screen]:
        pass

    @abstractmethod
    def update_kde_background(self, image_path: pathlib.Path) -> None:
        pass

    @abstractmethod
    def update_gnome_background(self, image_path: pathlib.Path) -> None:
        pass

    def update_background_image(self, image_path: pathlib.Path) -> None:
        match self.desktop_environment:
            case DesktopEnvironment.KDE:
                self.update_kde_background(image_path)
            case DesktopEnvironment.GNOME:
                self.update_gnome_background(image_path)
            case _:
                logging.error('Cannot update background image. Desktop environment not supported')

        return
