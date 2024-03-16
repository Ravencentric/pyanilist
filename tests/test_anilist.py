import time

import pytest
from pyanilist import (
    Anilist,
    HTTPStatusError,
    HttpUrl,
    MediaFormat,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
    ValidationError,
)


def test_anilist() -> None:
    time.sleep(3)
    media = Anilist().search("Attack on titan")
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source == MediaSource.MANGA
    assert media.type == MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


def test_anilist_with_type_constraint() -> None:
    time.sleep(3)
    media = Anilist().search("Attack on titan", type=MediaType.MANGA)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2009
    assert media.source == MediaSource.ORIGINAL
    assert media.type == MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/53390")


def test_anilist_with_some_constraints() -> None:
    time.sleep(3)
    media = Anilist().search(
        "violet evergarden", type=MediaType.MANGA, format=MediaFormat.NOVEL, status=MediaStatus.FINISHED
    )
    assert media.title.romaji == "Violet Evergarden"
    assert media.start_date.year == 2015
    assert media.source == MediaSource.ORIGINAL
    assert media.type == MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/97298")


def test_anilist_with_all_constraints() -> None:
    time.sleep(3)
    media = Anilist().search(
        "My Hero Academia",
        season=MediaSeason.SPRING,
        season_year=2016,
        type=MediaType.ANIME,
        format=MediaFormat.TV,
        status=MediaStatus.FINISHED,
    )
    assert media.title.romaji == "Boku no Hero Academia"
    assert media.start_date.year == 2016
    assert media.source == MediaSource.MANGA
    assert media.type == MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/21459")


def test_anilist_title_doesnt_exist() -> None:
    time.sleep(3)
    with pytest.raises(HTTPStatusError, match="Not Found."):
        Anilist().search("Title does not exist", type=MediaType.MANGA)


def test_anilist_bad_search_combo() -> None:
    time.sleep(3)
    with pytest.raises(HTTPStatusError, match="Not Found."):
        Anilist().search("Attack on titan", season_year=1999)


def test_anilist_wrong_input_types() -> None:
    time.sleep(3)
    with pytest.raises(ValidationError):
        Anilist().search(123456789, season_year="hello", type=True)  # type: ignore


def test_anilist_id() -> None:
    time.sleep(3)
    media = Anilist().get(16498)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source == MediaSource.MANGA
    assert media.type == MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


def test_anilist_bad_id() -> None:
    time.sleep(3)
    with pytest.raises(HTTPStatusError, match="400 Bad Request"):
        Anilist().get(9999999999)
