from __future__ import annotations

import pytest

from pyanilist import AniList, MediaNotFoundError, RateLimitError


@pytest.mark.vcr
def test_media_not_found_error_properties(anilist_client: AniList) -> None:
    try:
        anilist_client.get_media(id=000000)
    except MediaNotFoundError as e:
        assert e.message == "Not Found."
        assert e.status_code == 404


@pytest.mark.vcr
def test_media_not_found_error(anilist_client: AniList) -> None:
    with pytest.raises(MediaNotFoundError):
        anilist_client.get_media(id=000000)


@pytest.mark.vcr
def test_rate_limit_error(anilist_client: AniList) -> None:
    with pytest.raises(RateLimitError):
        while True:
            anilist_client.get_media(id=170942)
