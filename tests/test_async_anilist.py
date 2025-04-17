from __future__ import annotations

import datetime

import pytest

from pyanilist import (
    AsyncAniList,
    CharacterRole,
    CharacterSort,
    FuzzyDate,
    MediaCoverImage,
    MediaFormat,
    MediaNotFoundError,
    MediaSeason,
    MediaSort,
    MediaSource,
    MediaStatus,
    MediaTitle,
    MediaTrailer,
    MediaType,
    NoMediaArgumentsError,
    RateLimitError,
    RecommendationSort,
    StaffSort,
    StudioSort,
)


@pytest.mark.vcr
async def test_anilist_get_media(async_anilist_client: AsyncAniList) -> None:
    media = await async_anilist_client.get_media(id=99426)
    assert media.average_score == 84
    assert media.banner_image == "https://s4.anilist.co/file/anilistcdn/media/anime/banner/99426-KsFVCSwVC3x3.jpg"
    assert media.chapters is None
    assert media.country_of_origin == "JP"
    assert media.cover_image == MediaCoverImage(
        extra_large="https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx99426-ti5BL69Ip3kZ.png",
        large="https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx99426-ti5BL69Ip3kZ.png",
        medium="https://s4.anilist.co/file/anilistcdn/media/anime/cover/small/bx99426-ti5BL69Ip3kZ.png",
        color="#f1ae28",
    )
    assert isinstance(media.description, str)
    assert media.description.startswith(
        "Mari Tamaki is in her second year of high school and wants to start something."
    )
    assert media.duration == 24
    assert media.end_date == FuzzyDate(year=2018, month=3, day=27)
    assert media.episodes == 13
    assert isinstance(media.favourites, int)
    assert media.favourites >= 8000
    assert media.format is MediaFormat.TV
    assert media.genres == ("Adventure", "Comedy", "Drama")
    assert media.hashtag == "#よりもい"
    assert media.id == 99426
    assert media.id_mal == 35839
    assert media.is_adult is False
    assert media.is_licensed is True
    assert media.is_locked is False
    assert media.mean_score == 84
    assert media.next_airing_episode is None
    assert isinstance(media.popularity, int)
    assert media.popularity >= 139_000
    assert media.season is MediaSeason.WINTER
    assert media.season_year == 2018
    assert media.site_url == "https://anilist.co/anime/99426"
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
        id="tAYL5VNAJq0", site="youtube", thumbnail="https://i.ytimg.com/vi/tAYL5VNAJq0/hqdefault.jpg"
    )
    assert media.type is MediaType.ANIME
    assert isinstance(media.updated_at, datetime.datetime)
    assert media.volumes is None

    assert media.from_dict(media.to_dict()) == media
    assert media.from_json(media.to_json()) == media


@pytest.mark.vcr
async def test_anilist_get_media_sorted_by_id_desc(async_anilist_client: AsyncAniList) -> None:
    media = await async_anilist_client.get_media("Attack On Titan", sort=MediaSort.ID_DESC)
    assert media.title.english == "Attack on Titan Final Season THE FINAL CHAPTERS Special 2"
    assert media.site_url == "https://anilist.co/anime/162314"


@pytest.mark.vcr
async def test_anilist_get_all_media_sorted_by_id(async_anilist_client: AsyncAniList) -> None:
    ids = [
        1,
        5,
        6,
        7,
        16,
        19,
        20,
        21,
        26,
        29,
        30,
        32,
        33,
        47,
        48,
        57,
        59,
        66,
        115,
        116,
        117,
        118,
        121,
        134,
        141,
        147,
        153,
        154,
        160,
        164,
        165,
        170,
        182,
        194,
        199,
        205,
        207,
        210,
        223,
        225,
        226,
        227,
        232,
        237,
        239,
        241,
        245,
        268,
        269,
        270,
        302,
        308,
        322,
        323,
        329,
        338,
        339,
        344,
        356,
        371,
        372,
        376,
        387,
        390,
        392,
        393,
        416,
        430,
        431,
        433,
        437,
        440,
        457,
        467,
        468,
        483,
        487,
        488,
        489,
        499,
        512,
        513,
        515,
        522,
        523,
        543,
        544,
        559,
        570,
        572,
        578,
        585,
        587,
        597,
        598,
        617,
        634,
        644,
        650,
        658,
        732,
        759,
        777,
        785,
        788,
        790,
        791,
        801,
        813,
        820,
        855,
        857,
        875,
        877,
        879,
        885,
        889,
        917,
        918,
        934,
        941,
        953,
        957,
        974,
        975,
        976,
        1029,
        1033,
        1095,
        1107,
        1142,
        1143,
        1154,
        1182,
        1184,
        1188,
        1210,
        1251,
        1281,
        1288,
        1345,
        1347,
        1430,
        1459,
        1460,
        1462,
        1470,
        1482,
        1487,
        1489,
        1519,
        1530,
        1535,
        1542,
        1559,
        1575,
        1589,
        1689,
        1690,
        1691,
        1698,
        1723,
        1735,
        1764,
        1818,
        1827,
        1829,
        1832,
        1861,
        1888,
        1889,
        1914,
        1927,
        1935,
        1943,
        1944,
        2001,
        2002,
        2025,
        2043,
        2050,
        2051,
        2069,
        2099,
        2129,
        2147,
        2154,
        2158,
        2159,
        2164,
        2167,
        2202,
        2236,
        2251,
        2299,
        2300,
        2301,
        2312,
        2337,
        2418,
    ]
    results = async_anilist_client.get_all_media(
        id_in=ids,
        sort=MediaSort.ID_DESC,
    )
    assert [media.id async for media in results] == list(reversed(ids))


@pytest.mark.vcr
async def test_anilist_get_recommendations(async_anilist_client: AsyncAniList) -> None:
    results = async_anilist_client.get_recommendations(99426, sort=RecommendationSort.RATING_DESC)
    recommendations = [rec async for rec in results]
    assert recommendations[0].title.english == "Laid-Back Camp"
    assert recommendations[1].title.english == "K-ON!"


@pytest.mark.vcr
async def test_anilist_get_recommendations_with_null_rec(async_anilist_client: AsyncAniList) -> None:
    # See: https://github.com/Ravencentric/pyanilist/issues/29
    results = async_anilist_client.get_recommendations(20889, sort=RecommendationSort.RATING_DESC)
    recommendations = [rec async for rec in results]
    assert recommendations[0].title.english == "My Teen Romantic Comedy SNAFU"
    assert recommendations[1].title.english == "Makeine: Too Many Losing Heroines!"


@pytest.mark.vcr
async def test_anilist_get_relations(async_anilist_client: AsyncAniList) -> None:
    relations = async_anilist_client.get_relations(16498)
    titles = []
    async for relation in relations:
        titles.append(f"{relation.title} ({relation.relation_type})")
    assert titles == [
        "Attack on Titan (ADAPTATION)",
        "Attack on Titan Part I: Crimson Bow and Arrow (ALTERNATIVE)",
        "Attack on Titan Part II: Wings of Freedom (ALTERNATIVE)",
        "Attack on Titan Season 2 (SEQUEL)",
        "Attack on Titan: Junior High (SPIN_OFF)",
        "Attack on Titan OVA (SIDE_STORY)",
        "Attack on Titan ~Chronicle~ (SUMMARY)",
        "Attack on Titan: No Regrets (PREQUEL)",
        "Attack on Titan: Lost Girls (SIDE_STORY)",
        "Attack on Titan Picture Drama (OTHER)",
        "Chiyuki no Fashion Check (CHARACTER)",
    ]


@pytest.mark.vcr
async def test_anilist_get_studios(async_anilist_client: AsyncAniList) -> None:
    results = async_anilist_client.get_studios(99426, sort=StudioSort.ID)
    studios = [studio async for studio in results]
    assert studios[0].id == 11
    assert studios[0].is_animation_studio is True
    assert studios[0].is_main is True
    assert studios[0].name == "MADHOUSE"
    assert studios[1].id == 108
    assert studios[1].is_animation_studio is False
    assert studios[1].is_main is False
    assert studios[1].name == "Media Factory"


@pytest.mark.vcr
async def test_anilist_get_studios_with_is_main(async_anilist_client: AsyncAniList) -> None:
    studios = async_anilist_client.get_studios(99426, is_main=True)
    assert [studio.name async for studio in studios] == ["MADHOUSE"]


@pytest.mark.vcr
async def test_anilist_get_staffs(async_anilist_client: AsyncAniList) -> None:
    staffs = async_anilist_client.get_staffs(99426, sort=StaffSort.ID)
    assert [staff.id async for staff in staffs] == [
        95185,
        95869,
        95885,
        101064,
        101187,
        101187,
        101187,
        101465,
        101465,
        101759,
        103074,
        104500,
        105579,
        105579,
        105579,
        106297,
        106457,
        106638,
        107198,
        107198,
        107357,
        111459,
        116505,
        118427,
        118616,
    ]


@pytest.mark.vcr
async def test_anilist_get_airing_schedule(async_anilist_client: AsyncAniList) -> None:
    results = async_anilist_client.get_airing_schedule(99426)
    airing_schedules = [sched async for sched in results]
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
async def test_anilist_get_airing_schedule_with_not_yet_aired(async_anilist_client: AsyncAniList) -> None:
    results = async_anilist_client.get_airing_schedule(99426, not_yet_aired=True)
    assert [sched async for sched in results] == []


@pytest.mark.vcr
async def test_anilist_get_characters(async_anilist_client: AsyncAniList) -> None:
    characters = async_anilist_client.get_characters(99426, sort=CharacterSort.ID)
    assert [char.name.full async for char in characters if char.name is not None] == [
        "Mari Tamaki",
        "Shirase Kobuchizawa",
        "Hinata Miyake",
        "Yuzuki Shiraishi",
        "Kanae Maekawa",
        "Yumiko Samejima",
        "Tamiko Shiraishi",
        "Megumi Takahashi",
        "Rin Tamaki",
        "Gin Toudou",
        "Toshio Zaizen",
        "Chiaki Mukai",
        "Nobue Todoroki",
        "Yume Sasaki",
        "Dai Himi",
        "Takako Kobuchizawa",
        "Kimari no Haha",
        "Honami Yasumoto",
    ]


@pytest.mark.vcr
async def test_anilist_get_characters_with_role(async_anilist_client: AsyncAniList) -> None:
    characters = async_anilist_client.get_characters(99426, role=CharacterRole.MAIN)
    assert [char.name.full async for char in characters if char.name is not None] == [
        "Mari Tamaki",
        "Shirase Kobuchizawa",
        "Hinata Miyake",
        "Yuzuki Shiraishi",
    ]


@pytest.mark.vcr
async def test_media_not_found_error_properties(async_anilist_client: AsyncAniList) -> None:
    try:
        _ = await async_anilist_client.get_media(id=000000)
    except MediaNotFoundError as e:
        assert e.message == "Not Found."
        assert e.status_code == 404


@pytest.mark.vcr
async def test_media_not_found_error(async_anilist_client: AsyncAniList) -> None:
    with pytest.raises(MediaNotFoundError):
        _ = await async_anilist_client.get_media(id=000000)


@pytest.mark.vcr
async def test_rate_limit_error(async_anilist_client: AsyncAniList) -> None:
    with pytest.raises(RateLimitError):
        while True:
            _ = await async_anilist_client.get_media(id=170942)


async def test_get_media_no_parameters_error(async_anilist_client: AsyncAniList) -> None:
    with pytest.raises(NoMediaArgumentsError):
        _ = await async_anilist_client.get_media()


async def test_get_all_media_no_parameters_error(async_anilist_client: AsyncAniList) -> None:
    with pytest.raises(NoMediaArgumentsError):
        _ = [media.title async for media in async_anilist_client.get_all_media()]
