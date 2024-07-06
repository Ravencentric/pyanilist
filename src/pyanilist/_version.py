from __future__ import annotations

from typing_extensions import NamedTuple

from ._compat import metadata


class Version(NamedTuple):
    major: int
    minor: int
    micro: int


def _get_version() -> str:
    """
    Get the version of pyanilist
    """
    try:
        return metadata.version("pyanilist")

    except metadata.PackageNotFoundError:
        return "0.0.0"
