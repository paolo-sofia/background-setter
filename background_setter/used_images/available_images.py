from __future__ import annotations
from dataclasses import dataclass, field, asdict


@dataclass
class ImagesList:
    horizontal: list[str] = field(default_factory=list)
    vertical: list[str] = field(default_factory=list)

    @property
    def __dict__(self: ImagesList) -> dict[str, list[str]]:
        """Convert the dataclass to its dict representation.

        :return: Returning the dictionary representation of the object using the `asdict` function of the dataclasses
            package.
        """
        return asdict(self)
