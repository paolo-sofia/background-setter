#! /usr/bin/env python3

import argparse
import pathlib
import random
import tomllib
from datetime import date
from glob import glob
from typing import List, Any, Dict, Tuple

import cv2

from background_setter.client.client import BackgroundSetterClient
from background_setter.dektop.desktop import Desktop
from background_setter.screen.screen_orientation import ScreenOrientation


def validate_args(args: List[str]) -> bool:  # sourcery skip: use-any
    """
    The function checks if all the arguments in a list exist as valid paths.

    :param args: args is a list of strings that represent file paths. The function is checking if each path exists and
    returns True if all paths exist, otherwise it returns False
    :type args: List[str]
    :return: The function `validate_args` is returning a boolean value. It returns `True` if all the arguments in the
    input list `args` are non-empty strings that represent existing paths in the file system, and `False` otherwise.
    """
    for arg in args:
        if not arg or not pathlib.Path(arg).exists():
            return False
    return True


def load_config() -> Dict[str, Any]:
    """
    This function loads a TOML configuration file and returns its contents as a dictionary.
    :return: A dictionary containing the data loaded from the "config.toml" file.
    """
    with open("config.toml", "rb") as f:
        data = tomllib.load(f)
    return data


def get_all_images_orientation(folder_path: pathlib.Path) -> List[str]:
    """
    This function returns a list of file paths for all images in a given folder path with extensions of jpg, jpeg, or
    png.
    
    :param folder_path: The folder path is a pathlib.Path object that represents the directory where the images are
    stored
    :type folder_path: pathlib.Path
    :return: The function `get_all_images_orientation` returns a list of strings, where each string is the path to an
    image file in the specified folder path that has one of the extensions 'jpg', 'jpeg', or 'png'.
    """
    available_extensions: Tuple[str, str, str] = ('jpg', 'jpeg', 'png')

    images_available: List[str] = []
    for ext in available_extensions:
        str(folder_path / f'*.{ext}')
        images_available.extend(glob(str(folder_path / f'*.{ext}')))

    return images_available


if __name__ == '__main__':
    config: Dict[str, Any] = load_config()
    parser = argparse.ArgumentParser(
        prog='Background setter',
        description='Sets a new background image everyday')

    parser.add_argument('-v', '--vertical', type=str, default='/home/paolo/Nextcloud/Sfondi/Verticali')
    parser.add_argument('-o', '--horizontal', type=str, default='/home/paolo/Nextcloud/Sfondi/orizzontali')
    arguments = parser.parse_args([])
    if not validate_args(list(arguments.__dict__.values())):
        quit(-1)

    client: BackgroundSetterClient = BackgroundSetterClient(pathlib.Path(config['project']['used_images_path']))
    desktop: Desktop = Desktop()
    today: str = date.today().strftime('%Y-%m-%d')

    if client.used_images.last_update == today:
        quit()

    for scr in desktop.screens:
        path: str = arguments.vertical if scr.orientation == ScreenOrientation.VERTICAL else arguments.horizontal
        all_images: List[str] = get_all_images_orientation(pathlib.Path(path))
        available_images: List[str] = client.get_available_images(all_images, scr.orientation)

        image_path = random.choice(available_images)

        y_start, y_stop = scr.offset.y, scr.offset.y + scr.resolution.height
        x_start, x_stop = scr.offset.x, scr.offset.x + scr.resolution.width
        desktop.background_img[y_start: y_stop, x_start: x_stop, :] = \
            cv2.resize(cv2.imread(str(image_path)), (scr.resolution.width, scr.resolution.height))

        client.update_used_images(image_path, scr.orientation)
        client.update_used_images_last_update()

    desktop.save_new_background_image()
    desktop.window_protocol.update_background_image(pathlib.Path(config['project']['backgroun_path']).expanduser())
    client.dump_update_used_images()
