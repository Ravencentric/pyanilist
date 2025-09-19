from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any, ParamSpec, TypeAlias, TypeVar

from pyanilist._enums import MediaSort
from pyanilist._errors import InvalidMediaQueryError
from pyanilist._query import MEDIA_QUERY_VARS_SNAKE_CASE_TO_ANILIST_CASE
from pyanilist._types import Media, MediaID, MediaQueryKwargs, SortType

T = TypeVar("T")
P = ParamSpec("P")
JsonType: TypeAlias = "dict[str, JsonType] | list[JsonType] | str | int | float | bool | None"


def to_snake_case(string: str) -> str:
    """Convert lowerCamelCase to snake_case."""
    return "".join(f"_{char}" if char.isupper() else char for char in string).removeprefix("_").lower()


def normalize_anilist_data(data: JsonType) -> Any:
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
    match data:
        case dict():
            result = {}
            for k, v in data.items():
                if (val := normalize_anilist_data(v)) is not None:
                    result[to_snake_case(k)] = val
            return result or None

        case list():
            items = [normalized for i in data if (normalized := normalize_anilist_data(i)) is not None]
            return items or None

        case None | [] | {}:
            return None

        case _:
            return data


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
    match media:
        case str():
            pattern = r"^https:\/\/anilist\.co\/(anime|manga)\/(\d+)"
            if match := re.match(pattern, media.strip(), flags=re.IGNORECASE):
                return int(match.group(2))

            msg = f"Invalid media URL. Expected a URL like 'https://anilist.co/anime/{{id}}', but got {media!r}."
            raise ValueError(msg)

        case Media():
            return media.id

        case int():
            return media

        case _:
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


def to_anilist_vars(search: str | None, kwargs: MediaQueryKwargs) -> dict[str, Any]:
    """
    Convert search and Media query keyword arguments to AniList API variables.
    """
    variables: dict[str, Any] = {}

    if search:
        variables["search"] = search

    sort = kwargs.pop("sort", None)
    if sort_key := get_sort_key(sort, MediaSort):
        variables["sort"] = sort_key

    try:
        variables.update(
            (MEDIA_QUERY_VARS_SNAKE_CASE_TO_ANILIST_CASE[key], value)
            for key, value in kwargs.items()
            if value is not None
        )
    except KeyError as key:
        msg = f"Unexpected media query variable: {key!r}"
        raise InvalidMediaQueryError(msg) from None

    if not variables:
        msg = "The Media query requires at least one valid argument."
        raise InvalidMediaQueryError(msg)

    return variables
