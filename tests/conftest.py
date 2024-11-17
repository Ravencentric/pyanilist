from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyanilist import AniList

if TYPE_CHECKING:
    from typing_extensions import Generator


@pytest.fixture
def anilist_client() -> Generator[AniList]:
    with AniList() as anilist:
        yield anilist
