from __future__ import annotations

import datetime

import pytest
from pydantic_core import Url
from pydantic_extra_types.color import Color

from pyanilist import (
    AiringSchedule,
    AniList,
    FuzzyDate,
    MediaCoverImage,
    MediaFormat,
    MediaRelation,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaTitle,
    MediaTrailer,
    MediaType,
    RecommendationSort,
)


@pytest.mark.vcr
def test_anilist_get_media(anilist_client: AniList) -> None:
    media = anilist_client.get_media(id=99426)
    assert media.average_score == 84
    assert media.banner_image == Url("https://s4.anilist.co/file/anilistcdn/media/anime/banner/99426-KsFVCSwVC3x3.jpg")
    assert media.chapters is None
    assert media.country_of_origin == "JP"
    assert media.cover_image == MediaCoverImage(
        extra_large=Url("https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx99426-5jWTUs719lQN.png"),
        large=Url("https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx99426-5jWTUs719lQN.png"),
        medium=Url("https://s4.anilist.co/file/anilistcdn/media/anime/cover/small/bx99426-5jWTUs719lQN.png"),
        color=Color("#ffbb35"),
    )
    assert media.description.startswith(
        "Mari Tamaki is in her second year of high school and wants to start something."
    )
    assert media.duration == 24
    assert media.end_date == FuzzyDate(year=2018, month=3, day=27)
    assert media.episodes == 13
    assert media.favourites == 8057
    assert media.format is MediaFormat.TV
    assert media.genres == ("Adventure", "Comedy", "Drama")
    assert media.hashtag == "#よりもい"
    assert media.id == 99426
    assert media.id_mal == 35839
    assert media.is_adult is False
    assert media.is_licensed is True
    assert media.is_locked is False
    assert media.mean_score == 84
    assert media.next_airing_episode == AiringSchedule(id=None, airing_at=None, time_until_airing=None, episode=None)
    assert media.popularity == 139362
    assert media.season is MediaSeason.WINTER
    assert media.season_year == 2018
    assert media.site_url == Url("https://anilist.co/anime/99426")
    assert media.source is MediaSource.ORIGINAL
    assert media.start_date == FuzzyDate(year=2018, month=1, day=2)
    assert media.status is MediaStatus.FINISHED
    assert media.synonyms == (
        "Uchuu Yorimo Toui Basho",
        "Sora yorimo Tooi Basho",
        "Uchuu yori mo Tooi Basho",
        "Yorimoi",
        "מקום רחוק יותר מהיקום",
        "ตามหัวใจไปสุดขอบฟ้า",
        "ดินแดนที่ห่างไกลยิ่งกว่าอวกาศ",
    )
    assert media.title == MediaTitle(
        romaji="Sora yori mo Tooi Basho", english="A Place Further Than the Universe", native="宇宙よりも遠い場所"
    )
    assert media.trailer == MediaTrailer(
        id="tAYL5VNAJq0", site="youtube", thumbnail=Url("https://i.ytimg.com/vi/tAYL5VNAJq0/hqdefault.jpg")
    )
    assert media.type is MediaType.ANIME
    assert isinstance(media.updated_at, datetime.datetime)
    assert media.volumes is None


@pytest.mark.vcr
def test_anilist_get_recommendations(anilist_client: AniList) -> None:
    recommendations = tuple(anilist_client.get_recommendations(99426, sort=RecommendationSort.RATING_DESC))
    assert recommendations[0].title.english == "Laid-Back Camp"
    assert recommendations[1].title.english == "K-ON!"


@pytest.mark.vcr
def test_anilist_get_relations(anilist_client: AniList) -> None:
    relations = tuple(anilist_client.get_relations(99426))
    assert relations[0].relation_type is MediaRelation.ADAPTATION


@pytest.mark.vcr
def test_anilist_get_studios(anilist_client: AniList) -> None:
    studios = tuple(anilist_client.get_studios(99426))
    assert studios[0].id == 11
    assert studios[0].is_animation_studio is True
    assert studios[0].is_main is True
    assert studios[0].name == "MADHOUSE"
    assert studios[1].id == 108
    assert studios[1].is_animation_studio is False
    assert studios[1].is_main is False
    assert studios[1].name == "Media Factory"


@pytest.mark.vcr
def test_anilist_get_staffs(anilist_client: AniList) -> None:
    staffs = tuple(anilist_client.get_staffs(99426))
    assert staffs[0].site_url == Url("https://anilist.co/staff/105579")
    assert staffs[1].site_url == Url("https://anilist.co/staff/107198")
    assert staffs[2].site_url == Url("https://anilist.co/staff/101187")


@pytest.mark.vcr
def test_anilist_get_airing_schedule(anilist_client: AniList) -> None:
    airing_schedules = tuple(anilist_client.get_airing_schedule(99426))
    assert airing_schedules[0].episode == 1
    assert airing_schedules[1].episode == 2
    assert airing_schedules[2].episode == 3
    assert airing_schedules[3].episode == 4
    assert airing_schedules[4].episode == 5
    assert airing_schedules[5].episode == 6
    assert airing_schedules[6].episode == 7
    assert airing_schedules[7].episode == 8
    assert airing_schedules[8].episode == 9
    assert airing_schedules[9].episode == 10
    assert airing_schedules[10].episode == 11
    assert airing_schedules[11].episode == 12
    assert airing_schedules[12].episode == 13


@pytest.mark.vcr
def test_anilist_get_characters(anilist_client: AniList) -> None:
    characters = tuple(anilist_client.get_characters(99426))
    assert characters[0].name.full == "Mari Tamaki"
    assert characters[-1].name.full == "Honami Yasumoto"
