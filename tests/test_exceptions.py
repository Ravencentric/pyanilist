import pytest
from pyanilist import (
    AniList,
    HTTPStatusError,
    MediaType,
    ValidationError,
)

anilist = AniList(retries=1)


def test_anilist_title_doesnt_exist() -> None:
    with pytest.raises(HTTPStatusError, match="Not Found."):
        anilist.search("Title does not exist", type=MediaType.MANGA)


def test_anilist_bad_search_combo() -> None:
    with pytest.raises(HTTPStatusError, match="Not Found."):
        anilist.search("Attack on titan", season_year=1999)


def test_anilist_wrong_input_types() -> None:
    with pytest.raises(ValidationError):
        anilist.search(123456789, season_year="hello", type=True)  # type: ignore


def test_anilist_bad_id() -> None:
    with pytest.raises(HTTPStatusError, match="400 Bad Request"):
        anilist.get(9999999999)
