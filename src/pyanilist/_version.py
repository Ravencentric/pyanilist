from __future__ import annotations

from importlib.metadata import version

from typing_extensions import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    micro: int


__version__ = version("pyanilist")
__version_tuple__ = Version(*map(int, __version__.split(".")))
