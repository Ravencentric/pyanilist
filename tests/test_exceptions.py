from __future__ import annotations

import pytest

from pyanilist import (
    AniList,
    HTTPStatusError,
    ValidationError,
)

anilist = AniList(retries=1)


def test_anilist_bad_search_combo() -> None:
    with pytest.raises(HTTPStatusError):
        anilist.get("Attack on titan", season_year=1999)


def test_anilist_wrong_input_types() -> None:
    with pytest.raises(ValidationError):
        anilist.get(id=123456789, season_year="hello", type=True)  # type: ignore


def test_anilist_bad_id() -> None:
    with pytest.raises(HTTPStatusError):
        anilist.get(id=9999999999)
