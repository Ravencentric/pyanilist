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
        return HTML2Text(bodywidth=0).handle(description).strip()  # type: ignore


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
