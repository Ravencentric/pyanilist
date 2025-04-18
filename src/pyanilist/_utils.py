from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from functools import lru_cache
from typing import Any, ParamSpec, TypeVar

from boltons.iterutils import remap

from pyanilist._types import Media, MediaID, SortType

T = TypeVar("T")
P = ParamSpec("P")


def cache(func: Callable[P, T], /) -> Callable[P, T]:
    """
    Equivalent to functools.cache, just typed differently
    to preserve the original function's signature.
    """
    return lru_cache(maxsize=None, typed=True)(func)  # type: ignore[return-value]


@cache
def to_snake_case(string: str) -> str:
    """Convert lowerCamelCase to snake_case."""
    return "".join(f"_{char}" if char.isupper() else char for char in string).removeprefix("_").lower()


def normalize_anilist_data(data: Any) -> Any:  # `Any` because json can be anything.
    """
    Normalize the JSON response from AniList by removing fields with null or empty values
    and converting keys from lowerCamelCase to snake_case.

    AniList's API can return inconsistent null values for fields with subfields.
    Sometimes it returns individual nulls for each subfield, while other times
    it returns a single null for the parent field.

    This function addresses this inconsistency by recursively removing any key-value pairs
    where the value is `None`, an empty list (`[]`), or an empty dictionary (`{}`).
    Additionally, it converts all keys to snake_case for better Pythonic style.
    """

    def visitor(path: tuple[Any, ...], key: Any, value: Any) -> bool | tuple[str, Any]:
        """Visitor function for boltons.remap that'll be called for every item in the dictionary."""
        if value in [None, {}, []]:
            # Returning False drops the item entirely
            return False
        if key.__class__ is not str:
            # Return True keeps the value unchanged
            return True
        return to_snake_case(key), value

    return remap(data, visit=visitor)  # type: ignore[no-untyped-call]


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


def resolve_media_id(media: MediaID) -> int:
    """
    Resolve the media id.

    Parameters
    ----------
    media : MediaID
        The media

    Returns
    -------
    int
        Integer ID of the media

    """
    if isinstance(media, str):
        pattern = r"^https:\/\/anilist.co\/(anime|manga)\/(\d+)"
        match = re.match(pattern, media.strip(), flags=re.IGNORECASE)

        if match is None:
            msg = f"Invalid media URL. Expected a URL like 'https://anilist.co/anime/{{id}}', but got {media!r}."
            raise ValueError(msg)

        return int(match.group(2))
    if isinstance(media, Media):
        return media.id

    if isinstance(media, int):
        return media

    msg = f"Expected media to be an int, str, or Media object, but got {type(media).__name__}."
    raise TypeError(msg)


def get_sort_key(sort: SortType[T], typ: type[T]) -> tuple[T, ...] | None:
    """
    Process a sort variable and returns a tuple suitable for AniList's `sort` parameter.
    This lets us accept a wider range of inputs for the `sort` parameter, while still
    normalizing it to a tuple (or `None`).

    Parameters
    ----------
    sort : SortType[T]
        The sort variable to process. Can be a single item of type `T`,
        an iterable of items of type `T`, or None.
    typ : type[T]
        The expected type of the sort variable when a single item is provided.

    Returns
    -------
    tuple[T, ...] | None
        - None if `sort` is None.
        - A tuple containing a single item of type `T` if `sort` is an instance of `typ`.
        - A tuple containing all items from `sort` if `sort` is an iterable.

    Raises
    ------
    TypeError
        If `sort` is not None, not an instance of `typ`, and not an iterable.

    """
    if not sort:
        # Normalize falsy inputs (None, [], etc.) to None
        return None

    if isinstance(sort, typ):
        return (sort,)

    if isinstance(sort, Iterable) and not isinstance(sort, str):
        return tuple(sort)

    msg = f"Invalid sort key: {type(sort).__name__}"
    raise TypeError(msg)
