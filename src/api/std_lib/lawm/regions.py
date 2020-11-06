from dataclasses import dataclass
from typing import Any

from api.std_lib.lawm.base_parameter import ModelGeneralParameter


@dataclass
class Region:
    name: str


@dataclass
class Developed(Region):
    name: str = "developed"


@dataclass
class Latinamerica(Region):
    name: str = "latinamerica"


@dataclass
class Africa(Region):
    name: str = "africa"


@dataclass
class Asia(Region):
    name: str = "asia"
