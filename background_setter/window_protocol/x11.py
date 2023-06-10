import os
from typing import List

from background_setter.window_protocol.desktop_environment import DesktopEnvironment
from background_setter.window_protocol.window_protocol import WindowProtocol


class X11(WindowProtocol):
    def __init__(self, desktop_environment: DesktopEnvironment):
        super().__init__(desktop_environment)

    def update_gnome_background(self, image_path: str) -> None:
        """
        This function updates the GNOME desktop background image using the provided image path.

        :param image_path: The file path of the image that will be set as the GNOME desktop background
        :type image_path: str
        :return: `None`.
        """
        os.system("gsettings get org.gnome.desktop.background picture-uri")
        os.system(f"gsettings set org.gnome.desktop.background picture-uri '{image_path}'")
        os.system(f"gsettings set org.gnome.desktop.background picture-uri-dark '{image_path}'")
        return

    def update_kde_background(self, image_path: str) -> None:
        """
        This function updates the KDE desktop background by modifying a configuration file with a new image path.

        :param image_path: The path to the image file that will be set as the KDE desktop background
        :type image_path: str
        :return: nothing (`None`).
        """
        home: str = os.environ['HOME']
        with open(f'{home}/.config/plasma-org.kde.plasma.desktop-appletsrc', 'r') as f:
            lines: List[str] = f.readlines()

        for i, line in enumerate(lines):
            if 'Image=' in line:
                lines[i] = f'Image=file://{image_path}\n'
                break

        with open(f'{home}/.config/plasma-org.kde.plasma.desktop-appletsrc', 'w') as f:
            f.writelines(lines)
        return
