import os

from background_setter.window_protocol.window_protocol import WindowProtocol


class X11(WindowProtocol):
    pass

    def update_background_image(self, image_path: str) -> None:
        pass

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

    def update_kde_background(self) -> None:
        """
        This function updates the KDE desktop background by modifying a configuration file.

        Returns:
          `None`.
        """
        with open(f'{HOME}/.config/plasma-org.kde.plasma.desktop-appletsrc', 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if 'Image=' in line:
                lines[i] = f'Image=file://{self.background_path}\n'
                break

        with open(f'{HOME}/.config/plasma-org.kde.plasma.desktop-appletsrc', 'w') as f:
            f.writelines(lines)
        return
