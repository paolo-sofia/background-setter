from enum import StrEnum


class DesktopEnvironment(StrEnum):
    GNOME: str = 'gnome'
    KDE: str = 'kde'
    OTHER: str = 'other'
