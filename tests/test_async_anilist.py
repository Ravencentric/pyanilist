from pyanilist import (
    AsyncAniList,
    CharacterRole,
    HttpUrl,
    MediaFormat,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)

from .mock_descriptions import BloomIntoYouAnthologyDescriptions, BloomIntoYouDescriptions


async def test_anilist_anime() -> None:
    media = await AsyncAniList().search("Attack on titan", type=MediaType.ANIME)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


async def test_anilist_manga() -> None:
    media = await AsyncAniList().search("Attack on titan", type=MediaType.MANGA)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2009
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/53390")


async def test_anilist_with_some_constraints() -> None:
    media = await AsyncAniList().search(
        "violet evergarden", type=MediaType.MANGA, format=MediaFormat.NOVEL, status=MediaStatus.FINISHED
    )
    assert media.title.romaji == "Violet Evergarden"
    assert media.start_date.year == 2015
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.MANGA
    assert media.site_url == HttpUrl("https://anilist.co/manga/97298")


async def test_anilist_with_all_constraints() -> None:
    media = await AsyncAniList().search(
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


async def test_anilist_id() -> None:
    media = await AsyncAniList().get(16498)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.site_url == HttpUrl("https://anilist.co/anime/16498")


async def test_anilist_description() -> None:
    media = await AsyncAniList().get(106794)
    assert media.title.english == "Bloom Into You Anthology"
    assert media.start_date.year == 2018
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.MANGA
    assert media.description.default == BloomIntoYouAnthologyDescriptions.SANITIZED_DEFAULT
    assert media.description.html == BloomIntoYouAnthologyDescriptions.SANITIZED_HTML
    assert media.description.markdown == BloomIntoYouAnthologyDescriptions.MARKDOWN
    assert media.description.text == BloomIntoYouAnthologyDescriptions.TEXT
    assert media.relations[0].description.default == BloomIntoYouDescriptions.DEFAULT
    assert media.relations[0].description.html == BloomIntoYouDescriptions.HTML
    assert media.relations[0].description.markdown == BloomIntoYouDescriptions.MARKDOWN
    assert media.relations[0].description.text == BloomIntoYouDescriptions.TEXT
    assert media.site_url == HttpUrl("https://anilist.co/manga/106794")


async def test_anilist_characters() -> None:
    media = await AsyncAniList().get(20954)
    main_characters = [character.name.full for character in media.characters if character.role is CharacterRole.MAIN]
    assert media.title.english == "A Silent Voice"
    assert media.start_date.year == 2016
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert len(main_characters) == 2
    assert "Shouya Ishida" in main_characters
    assert "Shouko Nishimiya" in main_characters
    assert media.site_url == HttpUrl("https://anilist.co/anime/20954")
