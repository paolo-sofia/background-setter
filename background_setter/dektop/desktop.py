import os
import pathlib
from typing import List

import cv2
import numpy as np

from screen.screen import Screen
from screen.screen_resolution import ScreenResolution
from window_protocol.desktop_environment import DesktopEnvironment
from window_protocol.window_protocol import WindowProtocol
from window_protocol.window_protocol_factory import WindowProtocolFactory


class Desktop:
    BACKGROUND_PATH: pathlib.Path = pathlib.Path('~/.local/share/backgrounds/sfondo.jpg').expanduser()

    def __init__(self):
        self.desktop_environment: DesktopEnvironment = self.detect_desktop_environment()
        self.window_protocol: WindowProtocol = WindowProtocolFactory().create_window_protocol(self.desktop_environment)
        self.screens: List[Screen] = self.window_protocol.get_screens()
        self.screen_resolution: ScreenResolution = self.window_protocol.get_desktop_resolution()
        self.background_img: np.ndarray = np.empty((self.screen_resolution.height, self.screen_resolution.width, 3),
                                                   dtype=np.uint8)

    @staticmethod
    def detect_desktop_environment() -> DesktopEnvironment:
        """
        The function detects the current desktop environment and returns the corresponding enum value.
        :return: a value of the `DesktopEnvironment` enum type, which can be one of the following:
        `DesktopEnvironment.KDE`, `DesktopEnvironment.GNOME`, or `DesktopEnvironment.OTHER`.
        """
        desktop_env: List[str] = os.environ['XDG_CURRENT_DESKTOP'].lower().split(':')
        desktop_env: str = desktop_env[1] if len(desktop_env) > 1 else desktop_env[0]
        if desktop_env == DesktopEnvironment.KDE:
            return DesktopEnvironment.KDE
        elif desktop_env == DesktopEnvironment.GNOME:
            return DesktopEnvironment.GNOME
        else:
            return DesktopEnvironment.OTHER

    # def extract_only_used_images_from_json(self) -> None:
    #     used_images: Dict[str, List[str]] = {'horizontal': [], 'vertical': []}
    #     for date in self.used_images_json:
    #         for key in self.used_images_json[date]:
    #             used_images[key].extend(self.used_images_json[date][key])
    #     self.used_images = used_images
    #     return

    def save_new_background_image(self) -> None:
        """
        This function saves a background image to a specified path using OpenCV's `imwrite` function.
        :return: `None`.
        """
        cv2.imwrite(str(self.BACKGROUND_PATH), self.background_img)
        return
