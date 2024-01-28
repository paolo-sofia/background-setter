import datetime
import json
import pathlib
import re
import uuid
import zoneinfo
from dataclasses import fields

from screen.screen_orientation import ScreenOrientation
from used_images.available_images import ImagesList
from used_images.used_images import UsedImages


class BackgroundSetterClient:
    """A class for managing background images and their usage on a device.

        The BackgroundSetterClient class provides methods for initializing a unique device ID,
        loading and updating used images, and getting available images based on screen orientation.

        Args:
            used_images_path (pathlib.Path): The path to the directory where used images are stored.

        Attributes:
            available_images (ImagesList): An instance of the ImagesList class representing the available images.
            used_images_path (pathlib.Path): The path to the directory where used images are stored.
            device_id (str): A unique device ID.
            full_path (pathlib.Path): The full path to the used images file.
            used_images (UsedImages): An instance of the UsedImages class representing the used images.

        Methods:
            dataclass_from_dict(klass, dikt): Convert a dictionary to a dataclass instance.
            initialize_device_id(): Initialize a unique device ID.
            initialize_used_images(): Initialize the used images dictionary.
            get_available_images(all_images, orientation): Get a list of available images.
            update_used_images(image_path, orientation): Update the list of used images.
            update_used_images_last_update(): Update the last update date of used images.
            dump_update_used_images(): Dump the used images into a JSON file.
    """

    def __init__(self, used_images_path: pathlib.Path) -> None:
        self.available_images: ImagesList = ImagesList()
        self.used_images_path: pathlib.Path = used_images_path.expanduser()
        self.device_id: str = self.initialize_device_id()
        self.full_path: pathlib.Path = self.used_images_path / self.device_id
        self.used_images: UsedImages = self.initialize_used_images()

    def dataclass_from_dict(self, klass, dikt):
        try:
            fieldtypes = {f.name: f.type for f in fields(klass)}
            return klass(**{f: self.dataclass_from_dict(fieldtypes[f], dikt[f]) for f in dikt})
        except:
            return dikt

    def initialize_device_id(self) -> str:
        """Initialize a unique device ID by searching for existing device IDs in a directory and generating a new one if none are found.

        :return: The method `initialize_device_id` returns a string representing the device ID. If a device ID is found 
        in the `used_images_path` directory, it returns that ID. Otherwise, it generates a new device ID using the
        `uuid.uuid4()` method and returns it.
        """
        pattern: re.Pattern = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}.json",
                                         re.I)
        new_device_id: str = f"{uuid.uuid4()!s}.json"
        for file in self.used_images_path.glob("*.json"):
            if dev_uuid := pattern.search(str(file)):
                return dev_uuid.group()
        return new_device_id

    def initialize_used_images(self) -> UsedImages:
        """Initialize a dictionary of used images by loading data from a file if it exists, else creates an empty dict.

        :return: None is being returned.
        """
        if not self.full_path.exists():
            return UsedImages(ImagesList())

        with self.full_path.open("r") as f:
            used_images = json.load(f)
        return self.dataclass_from_dict(UsedImages, used_images)

    def get_available_images(self, all_images: list[str], orientation: ScreenOrientation) -> list[str]:
        """Get a list of available images by removing the used images based on the given screen orientation.

        :param all_images: A list of strings representing the file names of all available images.
        :param orientation: Represents the orientation of a screen. It can be HORIZONTAL or VERTICAL.
        """
        used_images: set[str] = set(self.used_images.images.horizontal) if orientation == ScreenOrientation.HORIZONTAL \
            else set(self.used_images.images.vertical)

        available_images: list[str] = list(set(all_images).difference(used_images))
        return available_images or all_images

    def update_used_images(self, image_path: str, orientation: ScreenOrientation) -> None:
        """Update a list of used images based on their orientation.

        :param image_path: A string representing the file path of an image that has been used in the program
        :type image_path: str
        :param orientation: ScreenOrientation is an enumerated type that represents the orientation of a screen. It can 
        have two possible values: HORIZONTAL or VERTICAL. This parameter is used to determine which list to append the 
        image_path to in the used_images object
        :type orientation: ScreenOrientation
        :return: `None`.
        """
        if orientation == ScreenOrientation.HORIZONTAL:
            self.used_images.images.horizontal.append(image_path)
        elif orientation == ScreenOrientation.VERTICAL:
            self.used_images.images.vertical.append(image_path)

    def update_used_images_last_update(self) -> None:
        """Update the last update date of used images to today's date.

        :return: `None`.
        """
        self.used_images.last_update = (datetime.datetime.now(tz=zoneinfo.ZoneInfo(key="Europe/Rome")).date()
                                        .strftime("%Y-%m-%d"))

    def dump_update_used_images(self) -> None:
        """Dump the used images into a JSON file.

        :return: `None`.
        """
        if not self.used_images_path.exists():
            self.used_images_path.mkdir(parents=True)

        with self.full_path.open("w", encoding = "utf-8") as f:
            json.dump(self.used_images.__dict__, f, ensure_ascii=False, indent=4)

        # NON CANCELLARE PORCODIO
        # available_imgs = list(set(all_imgs).difference(set(used_images[screen_orientation])))
        # print(available_imgs, len(available_imgs), len(all_imgs))
        # if len(available_imgs) == 0:
        #     available_imgs = all_imgs
        # print(available_imgs)
        # return available_imgs
