import os
import pathlib
from typing import List

import cv2
import numpy as np

from background_setter.screen.screen import Screen
from background_setter.screen.screen_resolution import ScreenResolution
from background_setter.window_protocol.desktop_environment import DesktopEnvironment
from background_setter.window_protocol.window_protocol import WindowProtocol
from background_setter.window_protocol.window_protocol_factory import WindowProtocolFactory


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
        desktop_env: str = os.environ['XDG_CURRENT_DESKTOP'].split(':')[1].lower()
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
        cv2.imwrite(str(self.BACKGROUND_PATH), self.background_img)
        return
