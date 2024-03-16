import pytest
from pyanilist import (
    AsyncAnilist,
    HTTPStatusError,
    MediaType,
    ValidationError,
)


async def test_anilist_title_doesnt_exist() -> None:
    with pytest.raises(HTTPStatusError, match="Not Found."):
        await AsyncAnilist().search("Title does not exist", type=MediaType.MANGA)


async def test_anilist_bad_search_combo() -> None:
    with pytest.raises(HTTPStatusError, match="Not Found."):
        await AsyncAnilist().search("Attack on titan", season_year=1999)


async def test_anilist_wrong_input_types() -> None:
    with pytest.raises(ValidationError):
        await AsyncAnilist().search(123456789, season_year="hello", type=True)  # type: ignore


async def test_anilist_bad_id() -> None:
    with pytest.raises(HTTPStatusError, match="400 Bad Request"):
        await AsyncAnilist().get(9999999999)
