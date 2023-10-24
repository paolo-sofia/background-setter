from enum import StrEnum


class DesktopEnvironment(StrEnum):
    GNOME: str = 'gnome'
    KDE: str = 'kde'
    HYPRLAND: str = "hyprland"
    OTHER: str = 'other'

