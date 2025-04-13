from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyanilist import AniList, AsyncAniList

if TYPE_CHECKING:
    from typing_extensions import AsyncGenerator, Generator


@pytest.fixture
def anilist_client() -> Generator[AniList]:
    with AniList() as anilist:
        yield anilist


@pytest.fixture
async def async_anilist_client() -> AsyncGenerator[AsyncAniList]:
    async with AsyncAniList() as anilist:
        yield anilist
