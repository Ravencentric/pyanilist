import pytest
from pyanilist import (
    AsyncAniList,
    HTTPStatusError,
    ValidationError,
)

anilist = AsyncAniList(retries=1)


async def test_anilist_bad_search_combo() -> None:
    with pytest.raises(HTTPStatusError):
        await anilist.search("Attack on titan", season_year=1999)


async def test_anilist_wrong_input_types() -> None:
    with pytest.raises(ValidationError):
        await anilist.search(123456789, season_year="hello", type=True)  # type: ignore


async def test_anilist_bad_id() -> None:
    with pytest.raises(HTTPStatusError):
        await anilist.get(9999999999)
