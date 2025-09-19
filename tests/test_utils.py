from __future__ import annotations

from typing import Any

import pytest

from pyanilist import InvalidMediaQueryError, Media, MediaSort, MediaTitle, RecommendationSort
from pyanilist._utils import get_sort_key, normalize_anilist_data, resolve_media_id, to_anilist_vars


def test_normalize_anilist_data() -> None:
    data: dict[str, Any] = {
        "data": {
            "Media": {
                "id": 53390,
                "idMal": 23390,
                "type": "MANGA",
                "format": "MANGA",
                "status": "FINISHED",
                "description": "...",
                "season": None,
                "seasonYear": None,
                "episodes": None,
                "duration": None,
                "chapters": 141,
                "volumes": 34,
                "countryOfOrigin": "JP",
                "isLicensed": True,
                "source": "ORIGINAL",
                "hashtag": None,
                "updatedAt": 1744575395,
                "bannerImage": "https://s4.anilist.co/file/anilistcdn/media/manga/banner/53390-6Uru5rrjh8zv.jpg",
                "genres": ["Action", "Drama", "Fantasy", "Mystery"],
                "synonyms": [
                    "SnK",
                    "AoT",
                ],
                "averageScore": 84,
                "meanScore": 84,
                "popularity": 206287,
                "isLocked": False,
                "trending": 1,
                "favourites": 20063,
                "isAdult": False,
                "siteUrl": "https://anilist.co/manga/53390",
                "trailer": None,
                "title": {"romaji": "Shingeki no Kyojin", "english": "Attack on Titan", "native": "進撃の巨人"},
                "tags": [
                    {
                        "id": 217,
                        "name": "Dystopian",
                        "description": "Partly or completely set in a society characterized by poverty, squalor or oppression.",  # noqa: E501
                        "category": "Setting-Time",
                        "rank": 94,
                        "isGeneralSpoiler": False,
                        "isMediaSpoiler": False,
                        "isAdult": False,
                        "userId": None,
                    },
                    {
                        "id": 111,
                        "name": "War",
                        "description": "Partly or completely set during wartime.",
                        "category": "Theme-Other",
                        "rank": 92,
                        "isGeneralSpoiler": False,
                        "isMediaSpoiler": True,
                        "isAdult": False,
                        "userId": None,
                    },
                    {
                        "id": 143,
                        "name": "Survival",
                        "description": "Centers around the struggle to live in spite of extreme obstacles.",
                        "category": "Theme-Other",
                        "rank": 89,
                        "isGeneralSpoiler": False,
                        "isMediaSpoiler": False,
                        "isAdult": False,
                        "userId": None,
                    },
                ],
                "startDate": {"year": 2009, "month": 9, "day": 9},
                "rankings": [
                    {
                        "id": 23273,
                        "rank": 103,
                        "type": "RATED",
                        "format": "MANGA",
                        "year": None,
                        "season": None,
                        "allTime": True,
                        "context": "highest rated all time",
                    },
                    {
                        "id": 23674,
                        "rank": 4,
                        "type": "POPULAR",
                        "format": "MANGA",
                        "year": None,
                        "season": None,
                        "allTime": True,
                        "context": "most popular all time",
                    },
                ],
                "externalLinks": [
                    {
                        "id": 50565,
                        "url": "https://kodansha.us/series/attack-on-titan/",
                        "site": "Kodansha",
                        "siteId": 182,
                        "type": "INFO",
                        "language": "English",
                        "color": "#000000",
                        "icon": "https://s4.anilist.co/file/anilistcdn/link/icon/182-58tlR0enOnty.png",
                        "notes": None,
                        "isDisabled": False,
                    },
                ],
                "endDate": {"year": 2021, "month": 4, "day": 9},
                "coverImage": {
                    "extraLarge": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx53390-1RsuABC34P9D.jpg",
                    "large": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx53390-1RsuABC34P9D.jpg",
                    "medium": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/small/bx53390-1RsuABC34P9D.jpg",
                    "color": "#d6431a",
                },
                "nextAiringEpisode": None,
                "streamingEpisodes": [],
            }
        }
    }

    assert normalize_anilist_data(data["data"]["Media"]) == {
        "id": 53390,
        "id_mal": 23390,
        "type": "MANGA",
        "format": "MANGA",
        "status": "FINISHED",
        "description": "...",
        "chapters": 141,
        "volumes": 34,
        "country_of_origin": "JP",
        "is_licensed": True,
        "source": "ORIGINAL",
        "updated_at": 1744575395,
        "banner_image": "https://s4.anilist.co/file/anilistcdn/media/manga/banner/53390-6Uru5rrjh8zv.jpg",
        "genres": ["Action", "Drama", "Fantasy", "Mystery"],
        "synonyms": [
            "SnK",
            "AoT",
        ],
        "average_score": 84,
        "mean_score": 84,
        "popularity": 206287,
        "is_locked": False,
        "trending": 1,
        "favourites": 20063,
        "is_adult": False,
        "site_url": "https://anilist.co/manga/53390",
        "title": {"romaji": "Shingeki no Kyojin", "english": "Attack on Titan", "native": "進撃の巨人"},
        "tags": [
            {
                "id": 217,
                "name": "Dystopian",
                "description": "Partly or completely set in a society characterized by poverty, squalor or oppression.",
                "category": "Setting-Time",
                "rank": 94,
                "is_general_spoiler": False,
                "is_media_spoiler": False,
                "is_adult": False,
            },
            {
                "id": 111,
                "name": "War",
                "description": "Partly or completely set during wartime.",
                "category": "Theme-Other",
                "rank": 92,
                "is_general_spoiler": False,
                "is_media_spoiler": True,
                "is_adult": False,
            },
            {
                "id": 143,
                "name": "Survival",
                "description": "Centers around the struggle to live in spite of extreme obstacles.",
                "category": "Theme-Other",
                "rank": 89,
                "is_general_spoiler": False,
                "is_media_spoiler": False,
                "is_adult": False,
            },
        ],
        "start_date": {"year": 2009, "month": 9, "day": 9},
        "rankings": [
            {
                "id": 23273,
                "rank": 103,
                "type": "RATED",
                "format": "MANGA",
                "all_time": True,
                "context": "highest rated all time",
            },
            {
                "id": 23674,
                "rank": 4,
                "type": "POPULAR",
                "format": "MANGA",
                "all_time": True,
                "context": "most popular all time",
            },
        ],
        "external_links": [
            {
                "id": 50565,
                "url": "https://kodansha.us/series/attack-on-titan/",
                "site": "Kodansha",
                "site_id": 182,
                "type": "INFO",
                "language": "English",
                "color": "#000000",
                "icon": "https://s4.anilist.co/file/anilistcdn/link/icon/182-58tlR0enOnty.png",
                "is_disabled": False,
            },
        ],
        "end_date": {"year": 2021, "month": 4, "day": 9},
        "cover_image": {
            "extra_large": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/large/bx53390-1RsuABC34P9D.jpg",
            "large": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/medium/bx53390-1RsuABC34P9D.jpg",
            "medium": "https://s4.anilist.co/file/anilistcdn/media/manga/cover/small/bx53390-1RsuABC34P9D.jpg",
            "color": "#d6431a",
        },
    }


def test_resolve_media_id() -> None:
    assert (
        resolve_media_id(Media(id=170942, site_url="https://anilist.co/anime/170942/Blue-Box/", title=MediaTitle()))
        == 170942
    )
    assert resolve_media_id(170942) == 170942
    assert resolve_media_id("https://anilist.co/anime/170942/Blue-Box/") == 170942
    assert resolve_media_id("https://anilist.co/manga/132182") == 132182

    with pytest.raises(
        ValueError,
        match="Invalid media URL. Expected a URL like 'https://anilist.co/anime/{id}', but got 'https://anilist.co/character/191241/Chinatsu-Kano'.",
    ):
        resolve_media_id("https://anilist.co/character/191241/Chinatsu-Kano")

    with pytest.raises(TypeError, match="Expected media to be an int, str, or Media object, but got NoneType."):
        resolve_media_id(None)  # type: ignore[arg-type]


def test_get_sort_key() -> None:
    assert get_sort_key([], RecommendationSort) is None
    assert get_sort_key(None, RecommendationSort) is None
    assert get_sort_key(RecommendationSort.RATING, RecommendationSort) == (RecommendationSort.RATING,)
    assert get_sort_key([RecommendationSort.RATING, RecommendationSort.ID], RecommendationSort) == (
        RecommendationSort.RATING,
        RecommendationSort.ID,
    )

    with pytest.raises(TypeError):
        get_sort_key(object(), RecommendationSort)

def test_to_anilist_vars() -> None:
    assert to_anilist_vars(None, {"id": 123}) == {"id": 123}
    assert to_anilist_vars("hola", {"id_mal": 123}) == {"search": "hola", "idMal": 123}
    assert to_anilist_vars(None, {"average_score": 80, "is_adult": False, "sort": MediaSort.ID, "genre": None}) == {
        "averageScore": 80,
        "isAdult": False,
        "sort": (MediaSort.ID,),
    }

    with pytest.raises(InvalidMediaQueryError, match="Unexpected media query variable: 'unexpected_key'"):
        to_anilist_vars(None, {"unexpected_key": 123})  # type: ignore[typeddict-unknown-key]

    with pytest.raises(InvalidMediaQueryError, match="The Media query requires at least one valid argument."):
        to_anilist_vars(None, {})
