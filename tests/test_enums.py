from __future__ import annotations

import pytest

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
    assert CharacterRole.MAIN.label == "Main"
    assert ExternalLinkType.INFO.label == "Info"
    assert MediaFormat.TV.label == "TV"
    assert MediaFormat.TV_SHORT.label == "TV Short"
    assert MediaFormat.ONE_SHOT.label == "One Shot"
    assert MediaFormat.OVA.label == "OVA"
    assert MediaFormat.ONA.label == "ONA"
    assert MediaRankType.POPULAR.label == "Popular"
    assert MediaRelation.SIDE_STORY.label == "Side Story"
    assert MediaSeason.WINTER.label == "Winter"
    assert MediaSource.LIGHT_NOVEL.label == "Light Novel"
    assert MediaStatus.NOT_YET_RELEASED.label == "Not Yet Released"
    assert MediaType.ANIME.label == "Anime"


def test_case_insensitive_lookup() -> None:
    assert CharacterRole("maIN") is CharacterRole.MAIN
    assert MediaStatus("Not_Yet_Released") is MediaStatus.NOT_YET_RELEASED


def test_enum_value_error() -> None:
    with pytest.raises(ValueError):
        CharacterRole("blahblah")

    with pytest.raises(ValueError):
        CharacterRole(1)  # type: ignore[arg-type]
