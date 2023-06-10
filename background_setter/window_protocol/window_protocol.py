import os
import re
import subprocess
from abc import ABC, abstractmethod

from background_setter.screen.screen_resolution import ScreenResolution
from background_setter.window_protocol.desktop_environment import DesktopEnvironment


class WindowProtocol(ABC):
    """
    The `WindowProtocol` class is an abstract base class that provides methods for detecting the current desktop
    environment, retrieving the current screen resolution, and updating the background image.
    """

    def __init__(self):
        self.desktop_environment: DesktopEnvironment = self.detect_desktop_environment()

    @staticmethod
    def detect_desktop_environment() -> DesktopEnvironment:
        """
        The function detects the current desktop environment and returns the corresponding enum value.
        :return: a value of the `DesktopEnvironment` enum type, which can be one of the following:
        `DesktopEnvironment.KDE`, `DesktopEnvironment.GNOME`, or `DesktopEnvironment.OTHER`.
        """
        desktop_env: str = os.environ['XDG_CURRENT_DESKTOP'].split(':')[1].lower()
        if desktop_env == DesktopEnvironment.KDE:
            return DesktopEnvironment.KDE
        elif desktop_env == DesktopEnvironment.GNOME:
            return DesktopEnvironment.GNOME
        else:
            return DesktopEnvironment.OTHER

    @staticmethod
    def get_desktop_resolution() -> ScreenResolution:
        """
        The function retrieves the current screen resolution of the desktop using the xrandr command in Python.
        :return: The function `get_desktop_resolution()` returns an instance of the `ScreenResolution` class, which
        represents the current screen resolution of the desktop. If the screen resolution cannot be determined, it
        returns a `ScreenResolution` instance with width and height set to 0.
        """
        output = iter(subprocess.Popen(['xrandr | grep current'], stdout=subprocess.PIPE, shell=True).stdout)
        for row in output:
            if screen_res := re.search(r'current \d+ x \d+', row.decode('UTF-8')):
                screen_res = [int(x) for x in re.findall(r'\d+', screen_res.group())]
                return ScreenResolution(*screen_res)
        return ScreenResolution(0, 0)

    @abstractmethod
    def update_background_image(self, image_path: str) -> None:
        """
        This is a placeholder function that takes in an image path and updates the background image.

        :param image_path: A string representing the file path of the new background image that needs to be updated
        """
        pass
