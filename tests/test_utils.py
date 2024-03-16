from pyanilist._utils import flatten, remove_null_fields


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
    flattened = flatten(characters, "role") # type: ignore
    assert flattened == [{
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
    }]


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