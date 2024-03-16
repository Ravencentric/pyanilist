from __future__ import annotations

from typing import Any

import httpx
from pydantic import validate_call
from tenacity import AsyncRetrying, stop_after_attempt, wait_incrementing

from .._enums import MediaFormat, MediaSeason, MediaStatus, MediaType
from .._models import Media
from .._query import query_string
from .._types import AnilistID, AnilistTitle, AnilistYear
from .._utils import flatten, remove_null_fields


class AsyncAnilist:
    def __init__(
        self, api_url: str = "https://graphql.anilist.co", retries: int = 5, **httpx_async_client_kwargs: Any
    ) -> None:
        """
        Async Anilist API client.

        Parameters
        ----------
        api_url : str, optional
            The URL of the Anilist API. Default is "https://graphql.anilist.co".
        retries : int, optional
            Number of times to retry a failed request before raising an error. Default is 5.
        httpx_async_client_kwargs : Any, optional
            Keyword arguments to pass to the internal [httpx.AsyncClient()](https://www.python-httpx.org/api/#asyncclient)
            used to make the POST request.
        """
        self.api_url = api_url
        self.retries = retries
        self.httpx_async_client_kwargs = httpx_async_client_kwargs

    async def _post_request(
        self,
        id: AnilistID | None = None,
        season: MediaSeason | None = None,
        season_year: AnilistYear | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
        title: AnilistTitle | None = None,
    ) -> httpx.Response:
        """
        Make a POST request to the Anilist API.

        Parameters
        ----------
        id : AnilistID, optional
            Anilist ID of the media as found in the URL: https://anilist.co/{type}/{id}. Default is None.
        season : MediaSeason | None, optional
            The season the media was initially released in. Default is None.
        season_year : AnilistYear | None, optional
            The season year the media was initially released in. Default is None.
        type : MediaType | None, optional
            The type of the media; anime or manga. Default is None.
        format : MediaFormat | None, optional
            The format the media was released in. Default is None.
        status : MediaStatus | None, optional
            The current releasing status of the media. Default is None.
        title : AnilistTitle | None, optional
            The string used for searching on Anilist. Default is None.

        Raises
        ------
        httpx._exceptions.*
            Any exception from the httpx._exceptions module may be raised
            in case of errors encountered during the POST request.

        Returns
        -------
        Response
            The response object from the Anilist API.
        """

        # map params with Anilist's
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
                async with httpx.AsyncClient(**self.httpx_async_client_kwargs) as client:
                    response = await client.post(self.api_url, json=payload)
                    response.raise_for_status()

        return response

    @staticmethod
    def _post_process_response(response: httpx.Response) -> dict[str, Any]:
        """
        Post-processes the response from Anilist API.

        Parameters
        ----------
        response : Response
            The response object received from Anilist API.

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
        title: AnilistTitle,
        season: MediaSeason | None = None,
        season_year: AnilistYear | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
    ) -> Media:
        """
        Search for media on Anilist based on the provided parameters.

        Parameters
        ----------
        title : AnilistTitle | None, optional
            The string used for searching on Anilist. Default is None.
        season : MediaSeason | None, optional
            The season the media was initially released in. Default is None.
        season_year : AnilistYear | None, optional
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
        pyanilist.exceptions.*
            Any exception from the pyanilist.exceptions module may be raised
            in case of errors encountered during the POST request.

        Returns
        -------
        Media
            A Media object representing the retrieved media information.
        """

        return Media.model_validate(
            self._post_process_response(
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
    async def get(self, id: AnilistID) -> Media:
        """
        Retrieve media information from Anilist based on it's ID.

        Parameters
        ----------
        id : int
            Anilist ID of the media as found in the URL: https://anilist.co/{type}/{id}.

        Raises
        ------
        ValidationError
            Invalid input
        pyanilist.exceptions.*
            Any exception from the pyanilist.exceptions module may be raised
            in case of errors encountered during the POST request.

        Returns
        -------
        Media
            A Media object representing the retrieved media information.
        """

        return Media.model_validate(
            self._post_process_response(
                await self._post_request(
                    id=id,
                )
            )
        )
