from __future__ import annotations

from pyanilist._utils import (
    flatten,
    markdown_formatter,
    remove_null_fields,
    sanitize_description,
    text_formatter,
    to_anilist_case,
)


def test_flatten() -> None:
    data = {
        "characters": {
            "edges": [
                {
                    "node": {
                        "id": 45887,
                        "name": {
                            "first": "Sasha",
                            "middle": None,
                            "last": "Blouse",
                            "full": "Sasha Blouse",
                            "native": "サシャ・ブラウス",
                        },
                        "image": {
                            "large": "https://s4.anilist.co/file/anilistcdn/character/large/b45887-QPtJH0KwqthW.jpg",
                            "medium": "https://s4.anilist.co/file/anilistcdn/character/medium/b45887-QPtJH0KwqthW.jpg",
                        },
                        "description": "__Initial Height:__ 168cm\n__Affiliations__: Survey Corps",
                        "gender": "Female",
                        "dateOfBirth": {"year": None, "month": 7, "day": 26},
                        "age": "16-",
                        "bloodType": None,
                        "siteUrl": "https://anilist.co/character/45887",
                    },
                    "role": "SUPPORTING",
                },
            ]
        }
    }

    characters = data["characters"]
    flattened = flatten(characters, "role")  # type: ignore
    assert flattened == [
        {
            "id": 45887,
            "name": {
                "first": "Sasha",
                "middle": None,
                "last": "Blouse",
                "full": "Sasha Blouse",
                "native": "サシャ・ブラウス",
            },
            "image": {
                "large": "https://s4.anilist.co/file/anilistcdn/character/large/b45887-QPtJH0KwqthW.jpg",
                "medium": "https://s4.anilist.co/file/anilistcdn/character/medium/b45887-QPtJH0KwqthW.jpg",
            },
            "description": "__Initial Height:__ 168cm\n__Affiliations__: Survey Corps",
            "gender": "Female",
            "dateOfBirth": {"year": None, "month": 7, "day": 26},
            "age": "16-",
            "bloodType": None,
            "siteUrl": "https://anilist.co/character/45887",
            "role": "SUPPORTING",
        }
    ]


def test_remove_null_fields() -> None:
    data = {
        "data": {
            "Media": {
                "id": 153288,
                "title": {"romaji": "Kaijuu 8-gou", "english": "Kaiju No.8"},
                "status": "NOT_YET_RELEASED",
                "description": "...",
                "averageScore": None,
                "startDate": {"year": 2024, "month": 4, "day": 13},
                "endDate": {"year": None, "month": None, "day": None},
                "episodes": None,
                "chapters": None,
                "volumes": None,
                "rankings": [],
                "characters": {"nodes": []},
            }
        }
    }

    assert remove_null_fields(data) == {
        "data": {
            "Media": {
                "id": 153288,
                "title": {"romaji": "Kaijuu 8-gou", "english": "Kaiju No.8"},
                "status": "NOT_YET_RELEASED",
                "description": "...",
                "startDate": {"year": 2024, "month": 4, "day": 13},
            }
        }
    }


# fmt: off
def test_formatters() -> None:
    assert sanitize_description("<unknown><br>hi<br />") == "<br>hi<br>"
    assert markdown_formatter("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!") == "Hello, [world](https://www.google.com/earth/)!"
    assert text_formatter("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!") == "Hello, world!"
    assert sanitize_description(None) is None
    assert sanitize_description(None) is None
    assert markdown_formatter(None) is None
    assert text_formatter(None) is None
# fmt: on


def test_query_variables_constructor() -> None:
    casemap = {
        "id": "id",
        "id_mal": "idMal",
        "start_date": "startDate",
        "end_date": "endDate",
        "season": "season",
        "season_year": "seasonYear",
        "type": "type",
        "format": "format",
        "status": "status",
        "episodes": "episodes",
        "chapters": "chapters",
        "duration": "duration",
        "volumes": "volumes",
        "is_adult": "isAdult",
        "genre": "genre",
        "tag": "tag",
        "minimum_tag_rank": "minimumTagRank",
        "tag_category": "tagCategory",
        "licensed_by": "licensedBy",
        "licensed_by_id": "licensedById",
        "average_score": "averageScore",
        "popularity": "popularity",
        "source": "source",
        "country_of_origin": "countryOfOrigin",
        "is_licensed": "isLicensed",
        "search": "search",
        "id_not": "id_not",
        "id_in": "id_in",
        "id_not_in": "id_not_in",
        "id_mal_not": "idMal_not",
        "id_mal_in": "idMal_in",
        "id_mal_not_in": "idMal_not_in",
        "start_date_greater": "startDate_greater",
        "start_date_lesser": "startDate_lesser",
        "start_date_like": "startDate_like",
        "end_date_greater": "endDate_greater",
        "end_date_lesser": "endDate_lesser",
        "end_date_like": "endDate_like",
        "format_in": "format_in",
        "format_not": "format_not",
        "format_not_in": "format_not_in",
        "status_in": "status_in",
        "status_not": "status_not",
        "status_not_in": "status_not_in",
        "episodes_greater": "episodes_greater",
        "episodes_lesser": "episodes_lesser",
        "duration_greater": "duration_greater",
        "duration_lesser": "duration_lesser",
        "chapters_greater": "chapters_greater",
        "chapters_lesser": "chapters_lesser",
        "volumes_greater": "volumes_greater",
        "volumes_lesser": "volumes_lesser",
        "genre_in": "genre_in",
        "genre_not_in": "genre_not_in",
        "tag_in": "tag_in",
        "tag_not_in": "tag_not_in",
        "tag_category_in": "tagCategory_in",
        "tag_category_not_in": "tagCategory_not_in",
        "licensed_by_in": "licensedBy_in",
        "licensed_by_id_in": "licensedById_in",
        "average_score_not": "averageScore_not",
        "average_score_greater": "averageScore_greater",
        "average_score_lesser": "averageScore_lesser",
        "popularity_not": "popularity_not",
        "popularity_greater": "popularity_greater",
        "popularity_lesser": "popularity_lesser",
        "source_in": "source_in",
        "sort": "sort",
    }

    for key, value in casemap.items():
        assert to_anilist_case(key) == value
