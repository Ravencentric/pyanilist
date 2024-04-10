from pyanilist import FuzzyDate


def test_fuzzy_date() -> None:
    assert FuzzyDate(year=2023, month=1, day=4).iso_format() == "2023-01-04"
    assert FuzzyDate(year=2023, month=1).iso_format() == "2023-01"
    assert FuzzyDate(year=2023).iso_format() == "2023"
    assert FuzzyDate().iso_format() == ""
