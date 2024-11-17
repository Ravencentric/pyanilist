from __future__ import annotations

from pyanilist import CharacterImage, CharacterName, FuzzyDate, MediaCoverImage, MediaTitle, StaffImage, StaffName


def test_fuzzy_date() -> None:
    assert FuzzyDate(year=2023, month=1, day=4).iso_format() == "2023-01-04"
    assert FuzzyDate(year=2023, month=1).iso_format() == "2023-01"
    assert FuzzyDate(year=2023).iso_format() == "2023"
    assert FuzzyDate().iso_format() == ""

    yyyymmdd = FuzzyDate(year=2023, month=1, day=4)
    assert yyyymmdd.to_int() == int(yyyymmdd) == 20230104
    assert yyyymmdd.iso_format() == str(yyyymmdd) == "2023-01-04"

    yyyymm = FuzzyDate(year=2023, month=1)
    assert yyyymm.to_int() == int(yyyymm) == 20230100
    assert yyyymm.iso_format() == str(yyyymm) == "2023-01"

    yyyy = FuzzyDate(year=2023)
    assert yyyy.to_int() == int(yyyy) == 20230000
    assert yyyy.iso_format() == str(yyyy) == "2023"

    empty = FuzzyDate()
    assert empty.to_int() == int(empty) == 10000000
    assert empty.iso_format() == str(empty) == ""


def test_media_title() -> None:
    assert str(MediaTitle(romaji="romaji", english="english", native="native")) == "english"
    assert str(MediaTitle(romaji="romaji", native="native")) == "romaji"
    assert str(MediaTitle(native="native")) == "native"


def test_media_cover_image() -> None:
    assert str(MediaCoverImage()) == ""
    assert (
        str(MediaCoverImage(extra_large="https://example.com/image.png", large="https://example.com/image2.png"))
        == "https://example.com/image.png"
    )
    assert str(MediaCoverImage(large="https://example.com/image2.png")) == "https://example.com/image2.png"


def test_staff_name() -> None:
    assert str(StaffName()) == ""
    assert str(StaffName(full="Example")) == "Example"


def test_staff_image() -> None:
    assert str(StaffImage()) == ""
    assert (
        str(StaffImage(large="https://example.com/image.png", medium="https://example.com/image2.png"))
        == "https://example.com/image.png"
    )
    assert str(StaffImage(medium="https://example.com/image2.png")) == "https://example.com/image2.png"


def test_character_name() -> None:
    assert str(CharacterName()) == ""
    assert str(CharacterName(full="Example")) == "Example"


def test_character_image() -> None:
    assert str(CharacterImage()) == ""
    assert (
        str(CharacterImage(large="https://example.com/image.png", medium="https://example.com/image2.png"))
        == "https://example.com/image.png"
    )
    assert str(CharacterImage(medium="https://example.com/image2.png")) == "https://example.com/image2.png"
