from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from boltons.iterutils import remap

if TYPE_CHECKING:
    from pyanilist._models import Media


def remove_null_fields(dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    AniList's `null` return is inconsistent for fields that have their own subfields.
    some of them will return each subfield as `null` while some of them
    will return a single null for the parent field.

    This will sort of "normalize" fields by removing keys where the value is
    `None`, empty list, or empty dictionary.
    """
    return remap(dictionary, lambda path, key, value: value not in [None, {}, []])  # type: ignore[no-any-return, no-untyped-call]


def to_anilist_case(var: str) -> str:
    """
    Anilist doesn't stick to a single casing.
    Most of it is camelCase but then there's some made up stuff in there too.
    So can do nothing but create a mapping from snake_case to anilistCase.

    Parameters
    ----------
    var : str
        A snake_case variable.

    Returns
    -------
    str
        Same thing but in anilist's case.

    """
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

    return casemap[var]


def resolve_media_id(media: int | str | Media) -> int:
    """
    Resolve the media id.

    Parameters
    ----------
    media : int | str | Media
        The media

    Returns
    -------
    int
        Integer ID of the media

    """
    if isinstance(media, str):
        pattern = r"https:\/\/anilist.co\/(anime|manga)\/(\d+)"
        match = re.match(pattern, media, re.IGNORECASE)

        if match is None:
            msg = f"Invalid media URL. Expected a URL like 'https://anilist.co/anime/{{id}}', got {media!r}."
            raise ValueError(msg)

        return int(match.group(2))
    else:
        return media if isinstance(media, int) else media.id
