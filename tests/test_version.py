from __future__ import annotations

import tomli

from pyanilist import __version__, __version_tuple__
from pyanilist._version import Version


def test_versions_match() -> None:
    pyproject_version: str = tomli.load(open("pyproject.toml", "rb"))["project"]["version"]
    pyproject_version_tuple = Version(*[int(i) for i in pyproject_version.split(".")])

    assert pyproject_version == __version__
    assert isinstance(__version_tuple__, Version)
    assert pyproject_version_tuple == __version_tuple__
