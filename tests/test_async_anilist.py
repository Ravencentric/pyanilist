from pyanilist import (
    AsyncAniList,
    CharacterRole,
    MediaFormat,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)

from .helpers import get_description


async def test_anilist_anime() -> None:
    media = await AsyncAniList().get("Attack on titan", type=MediaType.ANIME)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.start_date.iso_format() == "2013-04-07"
    assert media.end_date.iso_format() == "2013-09-28"
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert [(staff.name.full, staff.role) for staff in media.staff] == [
        ("Tetsurou Araki", "Director"),
        ("Yasuko Kobayashi", "Series Composition"),
        ("Youko Hikasa", "Theme Song Performance (ED1)"),
        ("Hiroyuki Sawano", "Music"),
        ("Hironori Tanaka", "Key Animation (eps 7, 21)"),
        ("Hajime Isayama", "Original Creator"),
        ("Mika Kobayashi", "Insert Song Performance"),
        ("Kyouji Asano", "Character Design"),
        ("Aimee Blackschleger", "Insert Song Performance"),
        ("Hiroyuki Tanaka", "Assistant Director"),
        ("Hiroyuki Tanaka", "Episode Director (eps 1, 10, 18, 21, 24)"),
        ("Cyua", "Insert Song Performance"),
        ("Seiichi Nakatani", "Key Animation (ep 25)"),
        ("Kouichi Arai", "Animation (ED1)"),
        ("Hiromi Katou", "Key Animation (ep 25)"),
        ("Mayu Fujimoto", "Key Animation (OP1, ep 1)"),
        ("Kazuhiro Miwa", "Key Animation (ED2)"),
        ("Hiroshi Seko", "Script (eps 3, 5-7, 10, 11, 15, 17, 18, 23)"),
        ("Tomohiro Hirata", "Key Animation (ep 25)"),
        ("Tomohiro Hirata", "Storyboard (eps 8, 19, 21, 25)"),
        ("Naoki Kobayashi", "Key Animation (ep 9)"),
        ("Toshirou Fujii", "Key Animation (ep 9)"),
        ("Shouko Yasuda", "Key Animation (eps 3, 4, 11, 15)"),
        ("Daizen Komatsuda", "Storyboard (ep 23)"),
        ("You Moriyama", "Key Animation (OP1)"),
    ]
    assert media.site_url.__str__() == "https://anilist.co/anime/16498"


async def test_anilist_manga() -> None:
    media = await AsyncAniList().get("Attack on titan", type=MediaType.MANGA)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2009
    assert media.start_date.iso_format() == "2009-09-09"
    assert media.end_date.iso_format() == "2021-04-09"
    assert media.source is MediaSource.ORIGINAL
    assert media.type is MediaType.MANGA
    assert [(staff.name.full, staff.role) for staff in media.staff] == [
        ("Hajime Isayama", "Story & Art"),
        ("Kouta Sannomiya", "Assistant"),
        ("Yuusuke Nomura", "Assistant"),
        ("Ko Ransom", "Translator (English)"),
        ("Erika Abreu", "Translator (Portuguese)"),
        ("Kouhei Nagashii", "Assistant"),
        ("Yuuji Kaba", "Assistant"),
        ("Kyuu Takahata", "Assistant"),
        ("Sylvain Chollet", "Translator (French)"),
        ("Tatsuya Endou", "Assistant"),
        ("Paweł Dybała", "Translator (Polish)"),
        ("Shintarou Kawakubo", "Editing"),
        ("Yifeng Zhang", "Translator (Chinese)"),
    ]
    assert media.site_url.__str__() == "https://anilist.co/manga/53390"


async def test_anilist_with_constraints() -> None:
    media = await AsyncAniList().get(
        "My Hero Academia",
        season=MediaSeason.SPRING,
        season_year=2016,
        type=MediaType.ANIME,
        format=MediaFormat.TV,
        status_in=[MediaStatus.FINISHED],
    )
    assert media.title.romaji == "Boku no Hero Academia"
    assert media.start_date.year == 2016
    assert media.start_date.iso_format() == "2016-04-03"
    assert media.end_date.iso_format() == "2016-06-26"
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert [(staff.name.full, staff.role) for staff in media.staff] == [
        ("Kouhei Horikoshi", "Original Creator"),
        ("Yousuke Kuroda", "Series Composition"),
        ("Kenji Nagasaki", "Director"),
        ("Yoshihiko Umakoshi", "Character Design"),
        ("Yoshihiko Umakoshi", "Chief Animation Director"),
        ("Yuuki Hayashi", "Music"),
        ("Shigemi Ikeda", "Art Director"),
        ("Yukiko Maruyama", "Art Director"),
        ("Masafumi Mima", "Sound Director"),
        ("Porno Graffitti", "Theme Song Performance (OP)"),
        ("Brian the Sun", "Theme Song Performance (ED)"),
        ("Ayana Nishino", "Animation Director (eps 2, 6, 9, 12)"),
        ("Tomoko Fukunaga", "Key Animation (eps 1, 6, 11)"),
        ("Kazuhiro Miwa", "Key Animation (OP, eps 1, 4, 11, 13)"),
        ("Asuka Hayashi", "Key Animation (eps 5, 12)"),
        ("Hakuyu Go", "Storyboard (OP, ep 12)"),
        ("Hakuyu Go", "Key Animation (OP, eps 2, 12)"),
        ("Hakuyu Go", "Episode Director (ep 12)"),
        ("Hakuyu Go", "Design Assistance (ep 10)"),
        ("Colleen Clinkenbeard", "ADR Director (English)"),
        ("Satomi Nakamura", "Storyboard (ep 8)"),
        ("Takashi Yamazaki", "Storyboard (ep 7)"),
        ("Shinji Ishihira", "Storyboard (ep 10)"),
        ("Katsuyuki Kodera", "Storyboard (eps 5, 9, 13)"),
        ("Kenji Nagasaki", "Storyboard (OP, ED, eps 1, 2)"),
    ]
    assert media.site_url.__str__() == "https://anilist.co/anime/21459"


async def test_anilist_id() -> None:
    media = await AsyncAniList().get(id=16498)
    assert media.title.romaji == "Shingeki no Kyojin"
    assert media.start_date.year == 2013
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert media.start_date.iso_format() == "2013-04-07"
    assert media.end_date.iso_format() == "2013-09-28"
    assert [(staff.name.full, staff.role) for staff in media.staff] == [
        ("Tetsurou Araki", "Director"),
        ("Yasuko Kobayashi", "Series Composition"),
        ("Youko Hikasa", "Theme Song Performance (ED1)"),
        ("Hiroyuki Sawano", "Music"),
        ("Hironori Tanaka", "Key Animation (eps 7, 21)"),
        ("Hajime Isayama", "Original Creator"),
        ("Mika Kobayashi", "Insert Song Performance"),
        ("Kyouji Asano", "Character Design"),
        ("Aimee Blackschleger", "Insert Song Performance"),
        ("Hiroyuki Tanaka", "Assistant Director"),
        ("Hiroyuki Tanaka", "Episode Director (eps 1, 10, 18, 21, 24)"),
        ("Cyua", "Insert Song Performance"),
        ("Seiichi Nakatani", "Key Animation (ep 25)"),
        ("Kouichi Arai", "Animation (ED1)"),
        ("Hiromi Katou", "Key Animation (ep 25)"),
        ("Mayu Fujimoto", "Key Animation (OP1, ep 1)"),
        ("Kazuhiro Miwa", "Key Animation (ED2)"),
        ("Hiroshi Seko", "Script (eps 3, 5-7, 10, 11, 15, 17, 18, 23)"),
        ("Tomohiro Hirata", "Key Animation (ep 25)"),
        ("Tomohiro Hirata", "Storyboard (eps 8, 19, 21, 25)"),
        ("Naoki Kobayashi", "Key Animation (ep 9)"),
        ("Toshirou Fujii", "Key Animation (ep 9)"),
        ("Shouko Yasuda", "Key Animation (eps 3, 4, 11, 15)"),
        ("Daizen Komatsuda", "Storyboard (ep 23)"),
        ("You Moriyama", "Key Animation (OP1)"),
    ]
    assert media.site_url.__str__() == "https://anilist.co/anime/16498"


async def test_anilist_description() -> None:
    media = await AsyncAniList().get(id=106794)
    assert media.title.english == "Bloom Into You Anthology"
    assert media.start_date.year == 2018
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.MANGA
    assert media.description.default == get_description(id=106794, ext="default")
    assert media.description.html == get_description(id=106794, ext="html")
    assert media.description.markdown == get_description(id=106794, ext="markdown")
    assert media.description.text == get_description(id=106794, ext="text")
    assert media.site_url.__str__() == "https://anilist.co/manga/106794"


async def test_anilist_characters() -> None:
    media = await AsyncAniList().get(id=20954)
    assert media.title.english == "A Silent Voice"
    assert media.start_date.year == 2016
    assert media.source is MediaSource.MANGA
    assert media.type is MediaType.ANIME
    assert [character.name.full for character in media.characters if character.role is CharacterRole.MAIN] == [
        "Shouya Ishida",
        "Shouko Nishimiya",
    ]
    assert media.site_url.__str__() == "https://anilist.co/anime/20954"
