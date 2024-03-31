from __future__ import annotations

from typing import Any

import httpx
from pydantic import validate_call
from tenacity import AsyncRetrying, stop_after_attempt, wait_incrementing

from .._enums import MediaFormat, MediaSeason, MediaStatus, MediaType
from .._models import Media
from .._query import query_string
from .._types import AniListID, AniListTitle, AniListYear, HTTPXAsyncClientKwargs
from .._utils import flatten, markdown_formatter, remove_null_fields, sanitize_description, text_formatter


class AsyncAniList:
    def __init__(
        self, api_url: str = "https://graphql.anilist.co", retries: int = 5, **kwargs: HTTPXAsyncClientKwargs
    ) -> None:
        """
        Async AniList API client.

        Parameters
        ----------
        api_url : str, optional
            The URL of the AniList API. Default is `https://graphql.anilist.co`.
        retries : int, optional
            Number of times to retry a failed request before raising an error. Default is 5.
        kwargs : HTTPXAsyncClientKwargs, optional
            Keyword arguments to pass to the underlying [httpx.AsyncClient()](https://www.python-httpx.org/api/#asyncclient)
            used to make the POST request.
        """
        self.api_url = api_url
        self.retries = retries
        self.kwargs = kwargs

    async def _post_request(
        self,
        id: AniListID | None = None,
        season: MediaSeason | None = None,
        season_year: AniListYear | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
        title: AniListTitle | None = None,
    ) -> httpx.Response:
        """
        Make a POST request to the AniList API.

        Parameters
        ----------
        id : AniListID, optional
            AniList ID of the media as found in the URL: `https://anilist.co/{type}/{id}`. Default is None.
        season : MediaSeason | None, optional
            The season the media was initially released in. Default is None.
        season_year : AniListYear | None, optional
            The season year the media was initially released in. Default is None.
        type : MediaType | None, optional
            The type of the media; anime or manga. Default is None.
        format : MediaFormat | None, optional
            The format the media was released in. Default is None.
        status : MediaStatus | None, optional
            The current releasing status of the media. Default is None.
        title : AniListTitle | None, optional
            The string used for searching on AniList. Default is None.

        Raises
        ------
        httpx._exceptions.*
            Any exception from the httpx._exceptions module may be raised
            in case of errors encountered during the POST request.

        Returns
        -------
        Response
            The response object from the AniList API.
        """

        # map params with AniList's
        query_variables = dict(
            id=id,
            season=season,
            seasonYear=season_year,
            type=type,
            format=format,
            status=status,
            search=title,
        )

        payload = {
            "query": query_string,
            "variables": {key: value for key, value in query_variables.items() if value is not None},
        }

        async for attempt in AsyncRetrying(
            stop=stop_after_attempt(self.retries),
            wait=wait_incrementing(start=0, increment=1),
            reraise=True,
        ):
            with attempt:
                async with httpx.AsyncClient(**self.kwargs) as client:
                    response = await client.post(self.api_url, json=payload)
                    response.raise_for_status()

        return response

    @staticmethod
    async def _process_description(dictionary: dict[str, Any]) -> dict[str, Any]:
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

    async def _post_process_response(self, response: httpx.Response) -> dict[str, Any]:
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
        dictionary["description"] = await self._process_description(dictionary)

        # Process description of every relation
        for relation in flattened_relations:
            relation["description"] = await self._process_description(relation)

        # replace the original
        dictionary["relations"] = flattened_relations
        dictionary["studios"] = flattened_studios
        dictionary["characters"] = flattened_characters
        dictionary["staff"] = flattened_staff

        # self explanatory, details on why
        # are in the function docstring
        return remove_null_fields(dictionary)

    @validate_call
    async def search(
        self,
        title: AniListTitle,
        season: MediaSeason | None = None,
        season_year: AniListYear | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
    ) -> Media:
        """
        Search for media on AniList based on the provided parameters.

        Parameters
        ----------
        title : AniListTitle
            The string used for searching on AniList.
        season : MediaSeason | None, optional
            The season the media was initially released in. Default is None.
        season_year : AniListYear | None, optional
            The season year the media was initially released in. Default is None.
        type : MediaType | None, optional
            The type of the media; anime or manga. Default is None.
        format : MediaFormat | None, optional
            The format the media was released in. Default is None.
        status : MediaStatus | None, optional
            The current releasing status of the media. Default is None.

        Raises
        ------
        ValidationError
            Invalid input
        HTTPStatusError
            AniList returned a non 2xx response.

        Returns
        -------
        Media
            A Media object representing the retrieved media information.
        """

        return Media.model_validate(
            await self._post_process_response(
                await self._post_request(
                    title=title,
                    season=season,
                    season_year=season_year,
                    type=type,
                    format=format,
                    status=status,
                )
            )
        )

    @validate_call
    async def get(self, id: AniListID) -> Media:
        """
        Retrieve media information from AniList based on it's ID.

        Parameters
        ----------
        id : int
            AniList ID of the media as found in the URL: `https://anilist.co/{type}/{id}`.

        Raises
        ------
        ValidationError
            Invalid input
        HTTPStatusError
            AniList returned a non 2xx response.

        Returns
        -------
        Media
            A Media object representing the retrieved media information.
        """

        return Media.model_validate(
            await self._post_process_response(
                await self._post_request(
                    id=id,
                )
            )
        )
