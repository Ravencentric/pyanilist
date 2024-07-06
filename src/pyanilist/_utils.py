from __future__ import annotations

import re
from typing import Any

import nh3
from boltons.iterutils import remap
from html2text import HTML2Text


def flatten(nested: dict[str, list[dict[str, dict[str, Any]]]] | None, key: str = "") -> list[dict[str, Any]]:
    """
    Flattens the nested dictionary returned by AniList's Media/Character/StaffConnection
    data types into a list of non-nested dictionaries.

    The media details we actually want are nested in ["edges"]["nodes"]
    while it's relation to the parent media is in ["edges"]. I find this unintuitive
    hence this flattening.

    If the above explanation doesn't make sense to you then you can get
    the idea by trying a query with Media/Character/StaffConnection on https://anilist.co/graphiql

    Parameters
    ----------
    nested : dict[str, list[dict[str, dict[str, Any]]]] | None, optional
        The nested dictionary structure to be flattened. If `None`, an empty list is returned.
    key : str, optional
        The key whose value should be moved into the "node" dictionary.
        If not provided, the function will only flatten the "node" dictionaries.

    Returns
    -------
    list[dict[str, Any]]
        A list of dictionaries, each containing the flattened structure of the original "node" dictionaries,
        with the optional key's value included if provided.

    Examples
    --------
    Given the following nested dictionary structure:

    ```
    "relations": { "edges": [ { "node": { "id": 105333 }, "isMain": "true" }, { "node": { "id": 107307 }, "isMain": "false" }]}
    ```
    The function will flatten it into:
    ```
    "relations": [ { "id": 105333, "isMain": "true" }, { "id": 107307, "isMain": "false" } ]
    ```

    """
    flattened = []

    if nested:
        edges = nested.get("edges")

        if edges:
            for dictionary in edges:
                node = dictionary.get("node")
                if node:
                    if key:
                        node[key] = dictionary.get(key)
                    flattened.append(node)

    return flattened


def sanitize_description(description: str | None) -> str | None:
    """
    Sanitize the description as it may contain
    arbitrary html elements
    """

    if description is None:
        return description
    else:
        return nh3.clean(description).strip()


def markdown_formatter(description: str | None) -> str | None:
    if description is None:
        return description
    else:
        return HTML2Text(bodywidth=0).handle(description).strip()


def text_formatter(description: str | None) -> str | None:
    if description is None:
        return description
    else:
        return re.sub(r"<.*?>", "", description).strip()


def remove_null_fields(dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    AniList's `null` return is inconsistent for fields that have their own subfields.
    some of them will return each subfield as `null` while some of them
    will return a single null for the parent field.

    This will sort of "normalize" fields by removing keys where the value is
    `None`, empty list, or empty dictionary.
    """
    return remap(dictionary, lambda path, key, value: value not in [None, {}, []])  # type: ignore


def to_anilist_case(var: str) -> str:
    """
    Anilist doesn't stick to a single casing.
    Most of it is camelCase but then there's some made up stuff in there too.
    So can do nothing but create a mapping from snake_case to anilistCase

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
