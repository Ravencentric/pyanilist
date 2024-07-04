from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ._utils import flatten, markdown_formatter, remove_null_fields, sanitize_description, text_formatter

if TYPE_CHECKING:  # pragma: no cover
    from httpx import Response


def process_description(dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Anilist's description field takes a parameter `asHtml: boolean`, effectively
    resulting in two differently formatted descriptions.

    Despite what the name implies, `asHtml` being `False` does not gurantee that there will be no `HTML`
    tags in the description.

    So we do a bit of post processing:
    - Sanitize the resulting descriptions
    - Introduce two more formats derived from the original two, i.e, markdown and plain text
    - Nest our newly acquired 4 descriptions into a single parent dictionary

    Example:

    This
    ```py
    {
        "defaultDescription": "...",
        "htmlDescription": "...",
    }
    ```
    Turns into this:
    ```py
    {
        "description": {
            "default": "...",
            "html": "...",
            "markdown": "...",
            "text": "...",
        }
    }
    ```py

    """

    default_description = sanitize_description(dictionary.get("defaultDescription"))
    html_description = sanitize_description(dictionary.get("htmlDescription"))
    markdown_description = markdown_formatter(html_description)
    text_description = text_formatter(default_description)

    # Delete the processed keys
    dictionary.pop("defaultDescription", None)
    dictionary.pop("htmlDescription", None)

    # Nest them inside a parent dictionary
    return dict(
        default=default_description,
        html=html_description,
        markdown=markdown_description,
        text=text_description,
    )


def post_process_response(response: Response) -> dict[str, Any]:
    """
    Post-processes the response from AniList API.

    Parameters
    ----------
    response : Response
        The response object received from AniList API.

    Returns
    -------
    dict[str, Any]
        Processed dictionary containing media information.

    Notes
    -----
    Currently, this function does two things:
    1. Flattening nested structures such as relations, studios, characters, and staff.
    2. Removing null fields to ensure a cleaner output.
    """

    # type hinting for IDE because it doesn't detect it automagically
    dictionary: dict[str, Any]

    dictionary = response.json()["data"]["Media"]

    # "Flatten" the nested list of dictionaries of list of dictionaries... blah blah
    # into simpler list for more intuitive access
    relations = dictionary.get("relations")
    dictionary.pop("relations", None)
    flattened_relations = flatten(relations, "relationType")

    # same thing here
    studios = dictionary.get("studios")
    dictionary.pop("studios", None)
    flattened_studios = flatten(studios, "isMain")

    # same thing here
    characters = dictionary.get("characters")
    dictionary.pop("characters", None)
    flattened_characters = flatten(characters, "role")

    # same thing here
    staff = dictionary.get("staff")
    dictionary.pop("staff", None)
    flattened_staff = flatten(staff, "role")

    # Process description
    dictionary["description"] = process_description(dictionary)

    # Process description of every relation
    for relation in flattened_relations:
        relation["description"] = process_description(relation)

    # replace the original
    dictionary["relations"] = flattened_relations
    dictionary["studios"] = flattened_studios
    dictionary["characters"] = flattened_characters
    dictionary["staff"] = flattened_staff

    # self explanatory, details on why
    # are in the function docstring
    return remove_null_fields(dictionary)
