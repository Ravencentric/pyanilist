from pyanilist import (
    CharacterRole,
    ExternalLinkType,
    MediaFormat,
    MediaRankType,
    MediaRelation,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)


def test_enums() -> None:
    assert CharacterRole.MAIN.title == "Main"
    assert ExternalLinkType.INFO.title == "Info"
    assert MediaFormat.TV.title == "TV"
    assert MediaFormat.TV_SHORT.title == "TV Short"
    assert MediaFormat.ONE_SHOT.title == "One Shot"
    assert MediaFormat.OVA.title == "OVA"
    assert MediaFormat.ONA.title == "ONA"
    assert MediaRankType.POPULAR.title == "Popular"
    assert MediaRelation.SIDE_STORY.title == "Side Story"
    assert MediaSeason.WINTER.title == "Winter"
    assert MediaSource.LIGHT_NOVEL.title == "Light Novel"
    assert MediaStatus.NOT_YET_RELEASED.title == "Not Yet Released"
    assert MediaType.ANIME.title == "Anime"
