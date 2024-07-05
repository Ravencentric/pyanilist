from pyanilist import FuzzyDate


def test_fuzzy_date() -> None:
    assert FuzzyDate(year=2023, month=1, day=4).iso_format() == "2023-01-04"
    assert FuzzyDate(year=2023, month=1).iso_format() == "2023-01"
    assert FuzzyDate(year=2023).iso_format() == "2023"
    assert FuzzyDate().iso_format() == ""

    assert FuzzyDate(year=2023, month=1, day=4).as_int() == 20230104
    assert FuzzyDate(year=2023, month=1).as_int() == 20230100
    assert FuzzyDate(year=2023).as_int() == 20230000
    assert FuzzyDate().as_int() == 10000000
