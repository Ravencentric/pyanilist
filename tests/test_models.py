from __future__ import annotations

from pyanilist import FuzzyDate, MediaTitle


def test_fuzzy_date() -> None:
    assert FuzzyDate(year=2023, month=1, day=4).iso_format() == "2023-01-04"
    assert FuzzyDate(year=2023, month=1).iso_format() == "2023-01"
    assert FuzzyDate(year=2023).iso_format() == "2023"
    assert FuzzyDate().iso_format() == ""

    yyyymmdd = FuzzyDate(year=2023, month=1, day=4)
    assert yyyymmdd.as_int() == int(yyyymmdd) == 20230104
    assert yyyymmdd.iso_format() == str(yyyymmdd) == "2023-01-04"

    yyyymm = FuzzyDate(year=2023, month=1)
    assert yyyymm.as_int() == int(yyyymm) == 20230100
    assert yyyymm.iso_format() == str(yyyymm) == "2023-01"

    yyyy = FuzzyDate(year=2023)
    assert yyyy.as_int() == int(yyyy) == 20230000
    assert yyyy.iso_format() == str(yyyy) == "2023"

    empty = FuzzyDate()
    assert empty.as_int() == int(empty) == 10000000
    assert empty.iso_format() == str(empty) == ""


def test_media_title() -> None:
    assert str(MediaTitle(romaji="romaji", english="english", native="native")) == "english"
    assert str(MediaTitle(romaji="romaji", native="native")) == "romaji"
    assert str(MediaTitle(native="native")) == "native"
