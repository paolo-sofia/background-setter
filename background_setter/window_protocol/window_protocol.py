import logging
import pathlib
import re
import subprocess
from abc import ABC, abstractmethod
from typing import List, Iterator

from screen.screen import Screen
from screen.screen_resolution import ScreenResolution
from window_protocol.desktop_environment import DesktopEnvironment


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
        """
        The function `get_screens()` returns a list of `Screen` objects.
        """
        pass

    @abstractmethod
    def update_kde_background(self, image_path: pathlib.Path) -> None:
        """
        This is a placeholder function that takes in an image path and updates the KDE background.

        :param image_path: The parameter `image_path` is of type `pathlib.Path` and represents the path to the image file
        that will be used as the new KDE desktop background
        :type image_path: pathlib.Path
        """
        pass

    @abstractmethod
    def update_gnome_background(self, image_path: pathlib.Path) -> None:
        """
        This is a placeholder function with no implementation to update the GNOME desktop background with an image.

        :param image_path: A pathlib.Path object representing the file path of the image to be used as the GNOME desktop
        background
        :type image_path: pathlib.Path
        """
        pass

    def update_background_image(self, image_path: pathlib.Path) -> None:
        """
        This function updates the background image of the desktop environment based on the type of environment.

        :param image_path: A pathlib.Path object representing the path to the new background image file
        :type image_path: pathlib.Path
        :return: `None`.
        """
        match self.desktop_environment:
            case DesktopEnvironment.KDE:
                self.update_kde_background(image_path)
            case DesktopEnvironment.GNOME:
                self.update_gnome_background(image_path)
            case _:
                logging.error('Cannot update background image. Desktop environment not supported')

        return
