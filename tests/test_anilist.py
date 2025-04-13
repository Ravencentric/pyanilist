from __future__ import annotations

import datetime

import pytest

from pyanilist import (
    AiringSchedule,
    AniList,
    CharacterRole,
    CharacterSort,
    FuzzyDate,
    MediaCoverImage,
    MediaFormat,
    MediaSeason,
    MediaSort,
    MediaSource,
    MediaStatus,
    MediaTitle,
    MediaTrailer,
    MediaType,
    RecommendationSort,
    StaffSort,
    StudioSort,
)


@pytest.mark.vcr
def test_anilist_get_media(anilist_client: AniList) -> None:
    media = anilist_client.get_media(id=99426)
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
    assert media.next_airing_episode == AiringSchedule(id=None, airing_at=None, time_until_airing=None, episode=None)
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


@pytest.mark.vcr
def test_anilist_get_media_sorted_by_id_desc(anilist_client: AniList) -> None:
    media = anilist_client.get_media("Attack On Titan", sort=MediaSort.ID_DESC)
    assert media.title.english == "Attack on Titan Final Season THE FINAL CHAPTERS Special 2"
    assert media.site_url == "https://anilist.co/anime/162314"


@pytest.mark.vcr
def test_anilist_get_all_media(anilist_client: AniList) -> None:
    results = anilist_client.get_all_media("fate")
    assert [(media.id, media.title.romaji) for media in results] == [
        (38764, "In Yeon"),
        (147359, "Inyeon"),
        (93544, "Minna Genki Kai!!"),
        (133235, "Meguri Awase"),
        (139074, "Unmei"),
        (74919, "Goen"),
        (159526, "Inyeon: Baramnan Cheo"),
        (20994, "GATE: Jieitai Kanochi nite, Kaku Tatakaeri"),
        (30314, "FAKE"),
        (176957, "Fake"),
        (130235, "FACE"),
        (44829, "Fake"),
        (36977, "GATE"),
        (102559, "Hua Jianghu: Huan Shi Men Sheng"),
        (71067, "Fake"),
        (93828, "Koibito no Jouken"),
        (35314, "Underground Kids: Gakuen Onmitsu Torimono"),
        (179153, "Fate Mate"),
        (365, "FAKE"),
        (163707, "FAKE"),
        (89719, "Aero"),
        (89733, "Bishoujo Hatsu Shibori"),
        (102876, "Face"),
        (90489, "Sate, Game Guard wo Kouryaku Shiyou ka."),
        (50006, "Fate/strange Fake"),
        (166617, "Fate/strange Fake"),
        (86753, "Fate/strange Fake"),
        (159832, "Unmyeong..(irago)hasyeotseumnida?!"),
        (98570, "Hate Mate"),
        (37314, "Koeru"),
        (115127, "Ima kara Kanojo ga Netoraremasu"),
        (100122, "Ao no Yokubou"),
        (114389, "Fate/strange Fake TVCM"),
        (123173, "Ore, Sono Kao Kirai desu"),
        (154966, "Fate/strange Fake: Whispers of Dawn"),
        (98830, "Omoichigai ga Koi no Tane"),
        (30530, "Snowdrop"),
        (19603, "Fate/stay night: Unlimited Blade Works"),
        (55191, "Fate/Zero"),
        (62425, "Fate/EXTRA"),
        (130670, "Nibanme no Unmei"),
        (133097, "Onnanoko Wa Venus"),
        (148193, "Jongcheonjiyeon"),
        (98035, "Fate/Apocrypha"),
        (94656, "Fate/Labyrinth"),
        (63005, "Fate/Apocrypha"),
        (87251, "Fate/Apocrypha"),
        (87905, "Unmei no Housoku"),
        (20791, "Fate/stay night [Heaven's Feel] I. presage flower"),
        (185007, "Geolsonjeon"),
        (116169, "Yu Wo Zhe"),
        (55999, "Shukumei no Partner"),
        (142350, "Jonmang Coin"),
        (10087, "Fate/Zero"),
        (151468, "Kudou no En"),
        (108493, "Fate/Requiem"),
        (33144, "Unmei ni Kiss"),
        (181655, "Oniai"),
        (68731, "Retaliating Molester Train"),
        (12565, "Fate/Prototype"),
        (43514, "Flower of Destiny"),
        (100552, "Daikirai, Daikirai, Daikirai"),
        (77881, "Prince no Shukumei"),
        (153991, "Fate:Lost Einherjar - Kyokkou no Aslaug"),
        (33649, "Fate/Zero"),
        (19165, "Fate/Zero Cafe"),
        (53568, "Fate/Extra"),
        (141862, "Mingyun Quan Tai"),
        (142870, "Fate/Ikustella  "),
        (171905, "Eogeureojin Hon"),
        (42828, "Unmei no Tori"),
    ]


@pytest.mark.vcr
def test_anilist_get_all_media_sorted_by_id(anilist_client: AniList) -> None:
    results = anilist_client.get_all_media("fate", sort=MediaSort.ID_DESC)
    assert [(media.id, media.title.romaji) for media in results] == [
        (185007, "Geolsonjeon"),
        (181655, "Oniai"),
        (179153, "Fate Mate"),
        (176957, "Fake"),
        (171905, "Eogeureojin Hon"),
        (166617, "Fate/strange Fake"),
        (163707, "FAKE"),
        (159832, "Unmyeong..(irago)hasyeotseumnida?!"),
        (159526, "Inyeon: Baramnan Cheo"),
        (154966, "Fate/strange Fake: Whispers of Dawn"),
        (153991, "Fate:Lost Einherjar - Kyokkou no Aslaug"),
        (151468, "Kudou no En"),
        (148193, "Jongcheonjiyeon"),
        (147359, "Inyeon"),
        (142870, "Fate/Ikustella  "),
        (142350, "Jonmang Coin"),
        (141862, "Mingyun Quan Tai"),
        (139074, "Unmei"),
        (133235, "Meguri Awase"),
        (133097, "Onnanoko Wa Venus"),
        (130670, "Nibanme no Unmei"),
        (130235, "FACE"),
        (123173, "Ore, Sono Kao Kirai desu"),
        (116169, "Yu Wo Zhe"),
        (115127, "Ima kara Kanojo ga Netoraremasu"),
        (114389, "Fate/strange Fake TVCM"),
        (108493, "Fate/Requiem"),
        (102876, "Face"),
        (102559, "Hua Jianghu: Huan Shi Men Sheng"),
        (100552, "Daikirai, Daikirai, Daikirai"),
        (100122, "Ao no Yokubou"),
        (98830, "Omoichigai ga Koi no Tane"),
        (98570, "Hate Mate"),
        (98035, "Fate/Apocrypha"),
        (94656, "Fate/Labyrinth"),
        (93828, "Koibito no Jouken"),
        (93544, "Minna Genki Kai!!"),
        (90489, "Sate, Game Guard wo Kouryaku Shiyou ka."),
        (89733, "Bishoujo Hatsu Shibori"),
        (89719, "Aero"),
        (87905, "Unmei no Housoku"),
        (87251, "Fate/Apocrypha"),
        (86753, "Fate/strange Fake"),
        (77881, "Prince no Shukumei"),
        (74919, "Goen"),
        (71067, "Fake"),
        (68731, "Retaliating Molester Train"),
        (63005, "Fate/Apocrypha"),
        (62425, "Fate/EXTRA"),
        (55999, "Shukumei no Partner"),
        (55191, "Fate/Zero"),
        (53568, "Fate/Extra"),
        (50006, "Fate/strange Fake"),
        (44829, "Fake"),
        (43514, "Flower of Destiny"),
        (42828, "Unmei no Tori"),
        (38764, "In Yeon"),
        (37314, "Koeru"),
        (36977, "GATE"),
        (35314, "Underground Kids: Gakuen Onmitsu Torimono"),
        (33649, "Fate/Zero"),
        (33144, "Unmei ni Kiss"),
        (30530, "Snowdrop"),
        (30314, "FAKE"),
        (20994, "GATE: Jieitai Kanochi nite, Kaku Tatakaeri"),
        (20791, "Fate/stay night [Heaven's Feel] I. presage flower"),
        (19603, "Fate/stay night: Unlimited Blade Works"),
        (19165, "Fate/Zero Cafe"),
        (12565, "Fate/Prototype"),
        (10087, "Fate/Zero"),
        (365, "FAKE"),
    ]


@pytest.mark.vcr
def test_anilist_get_recommendations(anilist_client: AniList) -> None:
    results = anilist_client.get_recommendations(99426, sort=RecommendationSort.RATING_DESC)
    recommendations = [rec for rec in results]
    assert recommendations[0].title.english == "Laid-Back Camp"
    assert recommendations[1].title.english == "K-ON!"


@pytest.mark.vcr
def test_anilist_get_recommendations_with_null_rec(anilist_client: AniList) -> None:
    # See: https://github.com/Ravencentric/pyanilist/issues/29
    results = anilist_client.get_recommendations(20889, sort=RecommendationSort.RATING_DESC)
    recommendations = [rec for rec in results]
    assert recommendations[0].title.english == "My Teen Romantic Comedy SNAFU"
    assert recommendations[1].title.english == "Makeine: Too Many Losing Heroines!"


@pytest.mark.vcr
def test_anilist_get_relations(anilist_client: AniList) -> None:
    relations = anilist_client.get_relations(16498)
    titles = []
    for relation in relations:
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
def test_anilist_get_studios(anilist_client: AniList) -> None:
    results = anilist_client.get_studios(99426, sort=StudioSort.ID)
    studios = [studio for studio in results]
    assert studios[0].id == 11
    assert studios[0].is_animation_studio is True
    assert studios[0].is_main is True
    assert studios[0].name == "MADHOUSE"
    assert studios[1].id == 108
    assert studios[1].is_animation_studio is False
    assert studios[1].is_main is False
    assert studios[1].name == "Media Factory"


@pytest.mark.vcr
def test_anilist_get_studios_with_is_main(anilist_client: AniList) -> None:
    studios = anilist_client.get_studios(99426, is_main=True)
    assert [studio.name for studio in studios] == ["MADHOUSE"]


@pytest.mark.vcr
def test_anilist_get_staffs(anilist_client: AniList) -> None:
    staffs = anilist_client.get_staffs(99426, sort=StaffSort.ID)
    assert [staff.id for staff in staffs] == [
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
def test_anilist_get_airing_schedule(anilist_client: AniList) -> None:
    results = anilist_client.get_airing_schedule(99426)
    airing_schedules = [sched for sched in results]
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
def test_anilist_get_airing_schedule_with_not_yet_aired(anilist_client: AniList) -> None:
    results = anilist_client.get_airing_schedule(99426, not_yet_aired=True)
    assert [sched for sched in results] == []


@pytest.mark.vcr
def test_anilist_get_characters(anilist_client: AniList) -> None:
    characters = anilist_client.get_characters(99426, sort=CharacterSort.ID)
    assert [char.name.full for char in characters] == [
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
def test_anilist_get_characters_with_role(anilist_client: AniList) -> None:
    characters = anilist_client.get_characters(99426, role=CharacterRole.MAIN)
    assert [char.name.full for char in characters] == [
        "Mari Tamaki",
        "Shirase Kobuchizawa",
        "Hinata Miyake",
        "Yuzuki Shiraishi",
    ]
