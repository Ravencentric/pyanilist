from pyanilist import (
    AniList,
    CharacterRole,
    HttpUrl,
    MediaFormat,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)


def test_anilist_anime() -> None:
    media = AniList().search("Attack on titan", type=MediaType.ANIME)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


def test_anilist_manga() -> None:
    media = AniList().search("Attack on titan", type=MediaType.MANGA)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2009
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/53390")


def test_anilist_with_some_constraints() -> None:
    media = AniList().search(
        "violet evergarden", type=MediaType.MANGA, format=MediaFormat.NOVEL, status=MediaStatus.FINISHED
    )
    assert media.title.romaji == "Violet Evergarden"
    assert media.start_date.year == 2015
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/97298")


def test_anilist_with_all_constraints() -> None:
    media = AniList().search(
        "My Hero Academia",
        season=MediaSeason.SPRING,
        season_year=2016,
        type=MediaType.ANIME,
        format=MediaFormat.TV,
        status=MediaStatus.FINISHED,
    )
    assert media.title.romaji == "Boku no Hero Academia"
    assert media.start_date.year == 2016
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/21459")


def test_anilist_id() -> None:
    media = AniList().get(16498)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


def test_anilist_description() -> None:
    media = AniList().get(99426)
    assert media.title.english == "A Place Further Than the Universe"
    assert media.start_date.year == 2018
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.ANIME
    assert media.description == (
        """Mari Tamaki is in her second year of high school and wants to start something. It's then that she meets Shirase, a girl with few friends who's considered weirdo by the rest of the class and nicknamed "Antarctic" since it's all she ever talks about. Unlike her peers, Mari is moved by Shirase's dedication and decides that even though it's unlikely that high school girls will ever go to Antarctica, she's going to try to go with Shirase.

(Source: Anime News Network)"""
    )
    assert media.relations[0].description == (
        """Mari Tamaki is in her second year of high school and wants to start something. It's then that she meets Shirase, a girl with few friends who's considered a weirdo by the rest of the class and nicknamed "Antarctica" since it's all she ever talks about. Unlike her peers, Mari is moved by Shirase's dedication and decides that even though it's unlikely that high school girls will ever go to Antarctica, she's going to try to go with Shirase.

Note: Includes two extra chapters."""
    )
    assert media.site_url == HttpUrl("https://anilist.co/anime/99426")


def test_anilist_characters() -> None:
    media = AniList().get(20954)
    main_characters = [character.name.full for character in media.characters if character.role is CharacterRole.MAIN]
    assert media.title.english == "A Silent Voice"
    assert media.start_date.year == 2016
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert len(main_characters) == 2
    assert "Shouya Ishida" in main_characters
    assert "Shouko Nishimiya" in main_characters
    assert media.site_url == HttpUrl("https://anilist.co/anime/20954")
