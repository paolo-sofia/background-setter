import logging
import os
from typing import Optional

from background_setter.window_protocol.desktop_environment import DesktopEnvironment
from background_setter.window_protocol.wayland import Wayland
from background_setter.window_protocol.window_protocol import WindowProtocol
from background_setter.window_protocol.window_protocol_type import WindowProtocolType
from background_setter.window_protocol.x11 import X11


class WindowProtocolFactory:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_window_protocol(desktop_environment: DesktopEnvironment) -> Optional[WindowProtocol]:
        """
        This function creates a window protocol object based on the desktop environment and session type.
        
        :param desktop_environment: The desktop environment is a parameter that specifies the type of desktop 
        environment being used, such as GNOME, KDE, or XFCE. It is used to create the appropriate window protocol class 
        for the given environment
        :type desktop_environment: DesktopEnvironment
        :return: an instance of a class that implements the WindowProtocol interface, which is either X11 or Wayland
        depending on the value of the XDG_SESSION_TYPE environment variable. If the session type is not supported, the
        function returns None.
        """
        match session_type := os.environ['XDG_SESSION_TYPE']:
            case WindowProtocolType.X11:
                return X11(desktop_environment)
            case WindowProtocolType.WAYLAND:
                return Wayland(desktop_environment)
            case _:
                logging.error(f'Cannot create window protocol class, {session_type} not yet supported')
                return None
