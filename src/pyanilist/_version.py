from __future__ import annotations

from typing import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    micro: int


__version__ = "0.6.1"
__version_tuple__ = Version(0, 6, 1)
