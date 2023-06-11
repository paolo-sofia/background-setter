import os
import pathlib
import re
import subprocess
from typing import List, Iterator

from background_setter.screen.screen import Screen
from background_setter.screen.screen_offset import ScreenOffset
from background_setter.screen.screen_resolution import ScreenResolution
from background_setter.window_protocol.desktop_environment import DesktopEnvironment
from background_setter.window_protocol.window_protocol import WindowProtocol


class X11(WindowProtocol):
    def __init__(self, desktop_environment: DesktopEnvironment):
        super().__init__(desktop_environment)

    @staticmethod
    def get_screens() -> List[Screen]:
        screen_list: List[Screen] = []
        output: Iterator[bytes] = iter(
            subprocess.Popen(['xrandr | grep connected'], stdout=subprocess.PIPE, shell=True).stdout)
        for row in output:
            if screen_info := re.search('\d+x\d+\+\d+\+\d+', row.decode('UTF-8')):
                screen_info = [int(x) for x in re.findall(r'\d+', screen_info.group())]
                screen_list.append(
                    Screen(
                        resolution=ScreenResolution(screen_info[0], screen_info[1]),
                        offset=ScreenOffset(screen_info[2], screen_info[3]))
                )
        return screen_list

    def update_gnome_background(self, image_path: pathlib.Path) -> None:
        """
        This function updates the GNOME desktop background image using the provided image path.

        :param image_path: The file path of the image that will be set as the GNOME desktop background
        :type image_path: str
        :return: `None`.
        """
        os.system("gsettings get org.gnome.desktop.background picture-uri")
        os.system(f"gsettings set org.gnome.desktop.background picture-uri '{str(image_path.absolute())}'")
        os.system(f"gsettings set org.gnome.desktop.background picture-uri-dark '{str(image_path.absolute())}'")
        return

    def update_kde_background(self, image_path: pathlib.Path) -> None:
        """
        This function updates the KDE desktop background by modifying a configuration file with a new image path.

        :param image_path: The path to the image file that will be set as the KDE desktop background
        :type image_path: str
        :return: nothing (`None`).
        """
        kde_config_file: str = f'{os.environ["HOME"]}/.config/plasma-org.kde.plasma.desktop-appletsrc'
        with open(kde_config_file, 'r') as f:
            lines: List[str] = f.readlines()

        for i, line in enumerate(lines):
            if 'Image=' in line:
                lines[i] = f'Image=file://{str(image_path.absolute())}\n'
                break

        with open(kde_config_file, 'w') as f:
            f.writelines(lines)
        return
