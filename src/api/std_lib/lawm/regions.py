from dataclasses import dataclass


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


DEFAULT_REGIONS = [Developed, Latinamerica, Africa, Asia]
