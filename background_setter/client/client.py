import datetime
import glob
import json
import pathlib
import re
import uuid
from typing import List, Set

from background_setter.screen.screen_orientation import ScreenOrientation
from background_setter.used_images.available_images import ImagesList
from background_setter.used_images.used_images import UsedImages


class BackgroundSetterClient:

    def __init__(self, used_images_path: pathlib.Path) -> None:
        self.available_images: ImagesList = ImagesList()
        self.used_images_path: pathlib.Path = used_images_path.expanduser()
        self.device_id: str = self.initialize_device_id()
        self.full_path: pathlib.Path = self.used_images_path / self.device_id
        self.used_images: UsedImages = self.initialize_used_images()

    def initialize_device_id(self) -> str:
        pattern: re.Pattern = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}.json',
                                         re.I)
        new_device_id: str = f"{str(uuid.uuid4())}.json"
        for file in glob.glob(str(self.used_images_path / '*.json')):
            if dev_uuid := pattern.search(file):
                return dev_uuid.group()
        return new_device_id

    def initialize_used_images(self) -> UsedImages:
        """
        This function initializes a dictionary of used images by loading data from a file if it exists, or creating an
        empty dictionary if it does not.
        :return: None is being returned.
        """
        if not self.full_path.exists():
            return UsedImages(ImagesList())

        with open(self.full_path, 'r') as f:
            used_images = json.load(f)
        return UsedImages(**used_images)

    def get_available_images(self, all_images: List[str], orientation: ScreenOrientation) -> List[str]:
        """
        This function returns a list of available images by subtracting the used images from all images based on the given
        screen orientation.

        :param all_images: A list of strings representing the file names of all available images
        :type all_images: List[str]
        :param orientation: The orientation parameter is of type ScreenOrientation, which is an enum that represents the
        orientation of a screen. It can have two possible values: ScreenOrientation.HORIZONTAL or ScreenOrientation.VERTICAL
        :type orientation: ScreenOrientation
        """

        used_images: Set[str] = set(self.used_images.images.horizontal) if orientation == ScreenOrientation.HORIZONTAL \
            else set(self.used_images.images.vertical)

        available_images: List[str] = list(set(all_images).difference(used_images))
        return available_images or all_images

    def update_used_images(self, image_path: str, orientation: ScreenOrientation) -> None:
        match orientation:
            case ScreenOrientation.HORIZONTAL:
                self.used_images.images.horizontal.append(image_path)
            case ScreenOrientation.VERTICAL:
                self.used_images.images.vertical.append(image_path)
        return

    def update_used_images_last_update(self) -> None:
        self.used_images.last_update = datetime.date.today().strftime('%Y-%m-%d')
        return

    def dump_update_used_images(self) -> None:
        if not self.used_images_path.exists():
            self.used_images_path.mkdir(parents=True)

        with open(self.full_path, 'w', encoding='utf-8') as f:
            json.dump(self.used_images.__dict__, f, ensure_ascii=False, indent=4)
        return

        # NON CANCELLARE PORCODIO
        # available_imgs = list(set(all_imgs).difference(set(used_images[screen_orientation])))
        # print(available_imgs, len(available_imgs), len(all_imgs))
        # if len(available_imgs) == 0:
        #     available_imgs = all_imgs
        # print(available_imgs)
        # return available_imgs
