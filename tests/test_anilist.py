from pyanilist import (
    Anilist,
    HttpUrl,
    MediaFormat,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)


def test_anilist() -> None:
    media = Anilist().search("Attack on titan", type=MediaType.ANIME)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source == MediaSource.MANGA
    assert media.type == MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


def test_anilist_with_type_constraint() -> None:
    media = Anilist().search("Attack on titan", type=MediaType.MANGA)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2009
    assert media.source == MediaSource.ORIGINAL
    assert media.type == MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/53390")


def test_anilist_with_some_constraints() -> None:
    media = Anilist().search(
        "violet evergarden", type=MediaType.MANGA, format=MediaFormat.NOVEL, status=MediaStatus.FINISHED
    )
    assert media.title.romaji == "Violet Evergarden"
    assert media.start_date.year == 2015
    assert media.source == MediaSource.ORIGINAL
    assert media.type == MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/97298")


def test_anilist_with_all_constraints() -> None:
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


def test_anilist_id() -> None:
    media = Anilist().get(16498)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source == MediaSource.MANGA
    assert media.type == MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")
