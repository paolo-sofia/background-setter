#! /usr/bin/env python3

import argparse
import configparser
import datetime
import pathlib
import random
import sys
import zoneinfo

import cv2
from background_setter.screen.screen import Screen
from background_setter.client.client import BackgroundSetterClient
from background_setter.dektop.desktop import Desktop
from background_setter.screen.screen_orientation import ScreenOrientation


def validate_args(args: list[str]) -> bool:    # sourcery skip: use-any
    """Check if all the arguments in a list exist as valid paths.

    :param args: args is a list of strings that represent file paths. The function is checking if each path exists and
    returns True if all paths exist, otherwise it returns False
    :type args: list[str]
    :return: The function `validate_args` is returning a boolean value. It returns `True` if all the arguments in the
    input list `args` are non-empty strings that represent existing paths in the file system, and `False` otherwise.
    """
    return next((False for arg in args if not arg or not pathlib.Path(arg).exists()), True)


def load_config() -> configparser.ConfigParser:
    """Load a configuration file and returns its contents as a dictionary.

    :return: A dictionary containing the data loaded from the "config.ini" file.
    """
    data = configparser.ConfigParser()
    data.read(pathlib.Path(__file__).parent.absolute() / "config.ini")
    return data


def get_all_images_orientation(folder_path: pathlib.Path) -> list[pathlib.Path | None]:
    """Return a list of file paths for all images in a given folder path with extensions of jpg, jpeg, or png.

    :param folder_path: The folder path is a pathlib.Path object that represents the directory where the images are
    stored
    :type folder_path: pathlib.Path
    :return: The function `get_all_images_orientation` returns a list of strings, where each string is the path to an
    image file in the specified folder path that has one of the extensions "jpg", "jpeg", or "png".
    """
    available_extensions: tuple[str, str, str] = ("jpg", "jpeg", "png")

    images_available: set[pathlib.Path | None] = set()
    for ext in available_extensions:
        images_available.update(pathlib.Path(folder_path).glob(f"*.{ext}"))

    return list(images_available)


def define_cli_args() -> argparse.ArgumentParser:
    """Define command-line arguments for a program that sets a new background image every day.

    :return: an instance of the `argparse.ArgumentParser` class.
    """
    arg_parser = argparse.ArgumentParser(
        prog = "Background setter",
        description = "Sets a new background image everyday"
    )

    arg_parser.add_argument("-v", "--vertical", type=str, default="/home/paolo/Nextcloud/Sfondi/Verticali")
    arg_parser.add_argument("-o", "--horizontal", type=str, default="/home/paolo/Nextcloud/Sfondi/orizzontali")
    return arg_parser


def resize_background_to_screen_resolution(desktop: Desktop, screen: Screen) -> None:
    """Resize the background image of a desktop to match the screen resolution.

    :param desktop: Represents the desktop object, which contains information about the current desktop state, such as
        the background image
    :param screen: Represents the screen or display on which the background image will be resized. It contains
        information about the screen's offset (position) and resolution (width and height)
    """
    y_start, y_stop = screen.offset.y, screen.offset.y + screen.resolution.height
    x_start, x_stop = screen.offset.x, screen.offset.x + screen.resolution.width
    desktop.background_img[y_start: y_stop, x_start: x_stop, :] = \
        cv2.resize(cv2.imread(str(image_path)), (screen.resolution.width, screen.resolution.height))


if __name__ == "__main__":
    config: configparser.ConfigParser = load_config()
    parser: argparse.ArgumentParser = define_cli_args()
    arguments: argparse.Namespace = parser.parse_args([])
    if not validate_args(list(arguments.__dict__.values())):
        sys.exit(-1)

    client: BackgroundSetterClient = BackgroundSetterClient(pathlib.Path(config["project"]["used_images_path"]))
    desktop: Desktop = Desktop()
    today: str = datetime.datetime.now(tz=zoneinfo.ZoneInfo(key="Europe/Rome")).date().strftime("%Y-%m-%d")
    if client.used_images.last_update == today:
        sys.exit()

    for scr in desktop.screens:
        path: str = arguments.vertical if scr.orientation == ScreenOrientation.VERTICAL else arguments.horizontal
        all_images: list[pathlib.Path | None] = get_all_images_orientation(pathlib.Path(path))
        available_images: list[str] = client.get_available_images(all_images, scr.orientation)

        image_path: str = str(random.choice(available_images))

        resize_background_to_screen_resolution(desktop, scr)

        client.update_used_images(image_path, scr.orientation)
        client.update_used_images_last_update()

    desktop.save_new_background_image()
    desktop.window_protocol.update_background_image(pathlib.Path(config["project"]["backgroun_path"]).expanduser())
    client.dump_update_used_images()
