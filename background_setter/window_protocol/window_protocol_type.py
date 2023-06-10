from enum import StrEnum


class WindowProtocolType(StrEnum):
    X11: str = 'x11'
    WAYLAND: str = 'wayland'
