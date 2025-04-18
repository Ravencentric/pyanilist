from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Any

import httpx
import msgspec
from httpx import AsyncClient

from pyanilist._enums import (
    CharacterRole,
    CharacterSort,
    MediaFormat,
    MediaSeason,
    MediaSort,
    MediaSource,
    MediaStatus,
    MediaType,
    RecommendationSort,
    StaffSort,
    StudioSort,
)
from pyanilist._errors import AnilistError, MediaNotFoundError, NoMediaArgumentsError, RateLimitError
from pyanilist._query import (
    AIRING_SCHEDULE_QUERY,
    ALL_MEDIA_QUERY,
    CHARACTERS_QUERY,
    MEDIA_QUERY,
    RECOMMENDATIONS_QUERY,
    RELATIONS_QUERY,
    STAFFS_QUERY,
    STUDIOS_QUERY,
)
from pyanilist._types import AiringSchedule, Character, Media, RelatedMedia, Staff, Studio
from pyanilist._utils import get_sort_key, normalize_anilist_data, resolve_media_id, to_anilist_case
from pyanilist._version import __version__

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterable

    from typing_extensions import Self

    from pyanilist._types import MediaID, SortType


class AsyncAniList:
    def __init__(self, api_url: str = "https://graphql.anilist.co", *, client: AsyncClient | None = None) -> None:
        """
        AniList API client.

        Parameters
        ----------
        api_url : str, optional
            The URL of the AniList API.
        client : AsyncClient | None, optional
            An [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient) instance
            used to make requests to AniList.

        """
        self._api_url = api_url
        self._client = (
            AsyncClient(headers={"Referer": "https://anilist.co", "User-Agent": f"pyanilist/{__version__}"})
            if client is None
            else client
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection."""
        await self._client.aclose()

    async def _post(self, *, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Utiliy function to POST to Anilist."""
        response = await self._client.post(self._api_url, json={"query": query, "variables": variables})
        data: dict[str, Any] = response.json()

        if "errors" in data:
            # As per Anilist's documentation: "Always check the errors field of the response
            # object... Even if you receive a status code of 200, you may still receive an error."
            # Therefore, we check for the 'errors' key to handle GraphQL-level errors, which may
            # occur even when the HTTP request is successful.
            #
            # Reference: https://docs.anilist.co/guide/graphql/errors#errors
            error = data["errors"][0]
            message = error["message"]
            status_code = error["status"]
            if status_code == httpx.codes.NOT_FOUND:
                raise MediaNotFoundError
            if status_code == httpx.codes.TOO_MANY_REQUESTS:
                # https://docs.anilist.co/guide/rate-limiting
                retry_after = int(response.headers["Retry-After"])
                raise RateLimitError(retry_after=retry_after)
            raise AnilistError(message=message, status_code=status_code)  # pragma: no cover

        return data["data"]  # type: ignore[no-any-return]

    async def get_media(  # noqa: PLR0913
        self,
        search: str | None = None,
        *,
        id: int | None = None,
        id_mal: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        season: MediaSeason | None = None,
        season_year: int | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
        episodes: int | None = None,
        chapters: int | None = None,
        duration: int | None = None,
        volumes: int | None = None,
        is_adult: bool | None = None,
        genre: str | None = None,
        tag: str | None = None,
        minimum_tag_rank: int | None = None,
        tag_category: str | None = None,
        licensed_by: str | None = None,
        licensed_by_id: int | None = None,
        average_score: int | None = None,
        popularity: int | None = None,
        source: MediaSource | None = None,
        country_of_origin: str | None = None,
        is_licensed: bool | None = None,
        id_not: int | None = None,
        id_in: Iterable[int] | None = None,
        id_not_in: Iterable[int] | None = None,
        id_mal_not: int | None = None,
        id_mal_in: Iterable[int] | None = None,
        id_mal_not_in: Iterable[int] | None = None,
        start_date_greater: int | None = None,
        start_date_lesser: int | None = None,
        start_date_like: str | None = None,
        end_date_greater: int | None = None,
        end_date_lesser: int | None = None,
        end_date_like: str | None = None,
        format_in: Iterable[MediaFormat] | None = None,
        format_not: MediaFormat | None = None,
        format_not_in: Iterable[MediaFormat] | None = None,
        status_in: Iterable[MediaStatus] | None = None,
        status_not: MediaStatus | None = None,
        status_not_in: Iterable[MediaStatus] | None = None,
        episodes_greater: int | None = None,
        episodes_lesser: int | None = None,
        duration_greater: int | None = None,
        duration_lesser: int | None = None,
        chapters_greater: int | None = None,
        chapters_lesser: int | None = None,
        volumes_greater: int | None = None,
        volumes_lesser: int | None = None,
        genre_in: Iterable[str] | None = None,
        genre_not_in: Iterable[str] | None = None,
        tag_in: Iterable[str] | None = None,
        tag_not_in: Iterable[str] | None = None,
        tag_category_in: Iterable[str] | None = None,
        tag_category_not_in: Iterable[str] | None = None,
        licensed_by_in: Iterable[str] | None = None,
        licensed_by_id_in: Iterable[int] | None = None,
        average_score_not: int | None = None,
        average_score_greater: int | None = None,
        average_score_lesser: int | None = None,
        popularity_not: int | None = None,
        popularity_greater: int | None = None,
        popularity_lesser: int | None = None,
        source_in: Iterable[MediaSource] | None = None,
        sort: SortType[MediaSort] = None,
    ) -> Media:
        """
        Retrieve a single media object from AniList based on the provided parameters.

        Parameters
        ----------
        search : str | None, optional
            Filter by search query.
        id : int | None, optional
            Filter by the media id.
        id_mal : int | None, optional
            Filter by the media's MyAnimeList id.
        start_date : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date : int | None, optional
            Filter by the end date of the media.
        season : MediaSeason | None, optional
            Filter by the season the media was released in.
        season_year : int | None, optional
            The year of the season (Winter 2017 would also include December 2016 releases). Requires season argument.
        type : MediaType | None, optional
            Filter by the media's type.
        format : MediaFormat | None, optional
            Filter by the media's format.
        status : MediaStatus | None, optional
            Filter by the media's current release status.
        episodes : int | None, optional
            Filter by amount of episodes the media has.
        chapters : int | None, optional
            Filter by the media's episode length.
        duration : int | None, optional
            Filter by the media's chapter count.
        volumes : int | None, optional
            Filter by the media's volume count.
        is_adult : bool | None, optional
            Filter by if the media's intended for 18+ adult audiences.
        genre : str | None, optional
            Filter by the media's genres.
        tag : str | None, optional
            Filter by the media's tags.
        minimum_tag_rank : int | None, optional
            Only apply the tags filter argument to tags above this rank. Default: 18.
        tag_category : str | None, optional
            Filter by the media's tags within a tag category.
        licensed_by : str | None, optional
            Filter media by sites name with a online streaming or reading license.
        licensed_by_id : int | None, optional
            Filter media by sites id with a online streaming or reading license.
        average_score : int | None, optional
            Filter by the media's average score.
        popularity : int | None, optional
            Filter by the number of users with this media on their list.
        source : MediaSource | None, optional
            Filter by the source type of the media.
        country_of_origin : str | None, optional
            Filter by the media's country of origin.
        is_licensed : bool | None, optional
            If the media is officially licensed or a self-published doujin release.
        id_not : int | None, optional
            Filter by the media id.
        id_in : Iterable[int] | None, optional
            Filter by the media id.
        id_not_in : Iterable[int] | None, optional
            Filter by the media id.
        id_mal_not : int | None, optional
            Filter by the media's MyAnimeList id.
        id_mal_in : Iterable[int] | None, optional
            Filter by the media's MyAnimeList id.
        id_mal_not_in : Iterable[int] | None, optional
            Filter by the media's MyAnimeList id.
        start_date_greater : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        start_date_lesser : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        start_date_like : str | None, optional
            Filter by the start date of the media.
        end_date_greater : int | None, optional
            Filter by the end date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date_lesser : int | None, optional
            Filter by the end date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date_like : str | None, optional
            Filter by the end date of the media.
        format_in : Iterable[MediaFormat] | None, optional
            Filter by the media's format.
        format_not : MediaFormat | None, optional
            Filter by the media's format.
        format_not_in : Iterable[MediaFormat] | None, optional
            Filter by the media's format.
        status_in : Iterable[MediaStatus] | None, optional
            Filter by the media's current release status.
        status_not : MediaStatus | None, optional
            Filter by the media's current release status.
        status_not_in : Iterable[MediaStatus] | None, optional
            Filter by the media's current release status.
        episodes_greater : int | None, optional
            Filter by amount of episodes the media has.
        episodes_lesser : int | None, optional
            Filter by amount of episodes the media has.
        duration_greater : int | None, optional
            Filter by the media's episode length.
        duration_lesser : int | None, optional
            Filter by the media's episode length.
        chapters_greater : int | None, optional
            Filter by the media's chapter count.
        chapters_lesser : int | None, optional
            Filter by the media's chapter count.
        volumes_greater : int | None, optional
            Filter by the media's volume count.
        volumes_lesser : int | None, optional
            Filter by the media's volume count.
        genre_in : Iterable[str] | None, optional
            Filter by the media's genres.
        genre_not_in : Iterable[str] | None, optional
            Filter by the media's genres.
        tag_in : Iterable[str] | None, optional
            Filter by the media's tags.
        tag_not_in : Iterable[str] | None, optional
            Filter by the media's tags.
        tag_category_in : Iterable[str] | None, optional
            Filter by the media's tags within a tag category.
        tag_category_not_in : Iterable[str] | None, optional
            Filter by the media's tags within a tag category.
        licensed_by_in : Iterable[str] | None, optional
            Filter media by sites name with a online streaming or reading license.
        licensed_by_id_in : Iterable[int] | None, optional
            Filter media by sites id with a online streaming or reading license.
        average_score_not : int | None, optional
            Filter by the media's average score.
        average_score_greater : int | None, optional
            Filter by the media's average score.
        average_score_lesser : int | None, optional
            Filter by the media's average score.
        popularity_not : int | None, optional
            Filter by the number of users with this media on their list.
        popularity_greater : int | None, optional
            Filter by the number of users with this media on their list.
        popularity_lesser : int | None, optional
            Filter by the number of users with this media on their list.
        source_in : Iterable[MediaSource] | None, optional
            Filter by the source type of the media.
        sort : SortType[MediaSort], optional
            The order the results will be returned in.
            Can be an instance of `MediaSort`, an iterable of `MediaSort`, or None.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        NoMediaArgumentsError
            If no media query arguments are provided.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        Returns
        -------
        Media
            An object representing the retrieved media.

        """

        variables = locals()
        variables.pop("self")
        variables = {to_anilist_case(key): value for key, value in variables.items() if value is not None}

        if sort_key := get_sort_key(sort, MediaSort):
            variables["sort"] = sort_key

        if not variables:
            raise NoMediaArgumentsError

        response = await self._post(
            query=MEDIA_QUERY,
            variables=variables,
        )

        return msgspec.convert(normalize_anilist_data(response["Media"]), type=Media, strict=False)

    async def get_all_media(  # noqa: PLR0913
        self,
        search: str | None = None,
        *,
        id: int | None = None,
        id_mal: int | None = None,
        start_date: int | None = None,
        end_date: int | None = None,
        season: MediaSeason | None = None,
        season_year: int | None = None,
        type: MediaType | None = None,
        format: MediaFormat | None = None,
        status: MediaStatus | None = None,
        episodes: int | None = None,
        chapters: int | None = None,
        duration: int | None = None,
        volumes: int | None = None,
        is_adult: bool | None = None,
        genre: str | None = None,
        tag: str | None = None,
        minimum_tag_rank: int | None = None,
        tag_category: str | None = None,
        licensed_by: str | None = None,
        licensed_by_id: int | None = None,
        average_score: int | None = None,
        popularity: int | None = None,
        source: MediaSource | None = None,
        country_of_origin: str | None = None,
        is_licensed: bool | None = None,
        id_not: int | None = None,
        id_in: Iterable[int] | None = None,
        id_not_in: Iterable[int] | None = None,
        id_mal_not: int | None = None,
        id_mal_in: Iterable[int] | None = None,
        id_mal_not_in: Iterable[int] | None = None,
        start_date_greater: int | None = None,
        start_date_lesser: int | None = None,
        start_date_like: str | None = None,
        end_date_greater: int | None = None,
        end_date_lesser: int | None = None,
        end_date_like: str | None = None,
        format_in: Iterable[MediaFormat] | None = None,
        format_not: MediaFormat | None = None,
        format_not_in: Iterable[MediaFormat] | None = None,
        status_in: Iterable[MediaStatus] | None = None,
        status_not: MediaStatus | None = None,
        status_not_in: Iterable[MediaStatus] | None = None,
        episodes_greater: int | None = None,
        episodes_lesser: int | None = None,
        duration_greater: int | None = None,
        duration_lesser: int | None = None,
        chapters_greater: int | None = None,
        chapters_lesser: int | None = None,
        volumes_greater: int | None = None,
        volumes_lesser: int | None = None,
        genre_in: Iterable[str] | None = None,
        genre_not_in: Iterable[str] | None = None,
        tag_in: Iterable[str] | None = None,
        tag_not_in: Iterable[str] | None = None,
        tag_category_in: Iterable[str] | None = None,
        tag_category_not_in: Iterable[str] | None = None,
        licensed_by_in: Iterable[str] | None = None,
        licensed_by_id_in: Iterable[int] | None = None,
        average_score_not: int | None = None,
        average_score_greater: int | None = None,
        average_score_lesser: int | None = None,
        popularity_not: int | None = None,
        popularity_greater: int | None = None,
        popularity_lesser: int | None = None,
        source_in: Iterable[MediaSource] | None = None,
        sort: SortType[MediaSort] = None,
    ) -> AsyncIterator[Media]:
        """
        Retrieve all matching media from AniList based on the provided parameters as an iterator.

        Unlike [`AsyncAniList.get_media`][pyanilist.AsyncAniList.get_media],
        this method does not raise a [`MediaNotFoundError`][pyanilist.MediaNotFoundError]
        if no media entries are found; instead, the iterator will simply be empty.

        Parameters
        ----------
        search : str | None, optional
            Filter by search query.
        id : int | None, optional
            Filter by the media id.
        id_mal : int | None, optional
            Filter by the media's MyAnimeList id.
        start_date : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date : int | None, optional
            Filter by the end date of the media.
        season : MediaSeason | None, optional
            Filter by the season the media was released in.
        season_year : int | None, optional
            The year of the season (Winter 2017 would also include December 2016 releases). Requires season argument.
        type : MediaType | None, optional
            Filter by the media's type.
        format : MediaFormat | None, optional
            Filter by the media's format.
        status : MediaStatus | None, optional
            Filter by the media's current release status.
        episodes : int | None, optional
            Filter by amount of episodes the media has.
        chapters : int | None, optional
            Filter by the media's episode length.
        duration : int | None, optional
            Filter by the media's chapter count.
        volumes : int | None, optional
            Filter by the media's volume count.
        is_adult : bool | None, optional
            Filter by if the media's intended for 18+ adult audiences.
        genre : str | None, optional
            Filter by the media's genres.
        tag : str | None, optional
            Filter by the media's tags.
        minimum_tag_rank : int | None, optional
            Only apply the tags filter argument to tags above this rank. Default: 18.
        tag_category : str | None, optional
            Filter by the media's tags within a tag category.
        licensed_by : str | None, optional
            Filter media by sites name with a online streaming or reading license.
        licensed_by_id : int | None, optional
            Filter media by sites id with a online streaming or reading license.
        average_score : int | None, optional
            Filter by the media's average score.
        popularity : int | None, optional
            Filter by the number of users with this media on their list.
        source : MediaSource | None, optional
            Filter by the source type of the media.
        country_of_origin : str | None, optional
            Filter by the media's country of origin.
        is_licensed : bool | None, optional
            If the media is officially licensed or a self-published doujin release.
        id_not : int | None, optional
            Filter by the media id.
        id_in : Iterable[int] | None, optional
            Filter by the media id.
        id_not_in : Iterable[int] | None, optional
            Filter by the media id.
        id_mal_not : int | None, optional
            Filter by the media's MyAnimeList id.
        id_mal_in : Iterable[int] | None, optional
            Filter by the media's MyAnimeList id.
        id_mal_not_in : Iterable[int] | None, optional
            Filter by the media's MyAnimeList id.
        start_date_greater : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        start_date_lesser : int | None, optional
            Filter by the start date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        start_date_like : str | None, optional
            Filter by the start date of the media.
        end_date_greater : int | None, optional
            Filter by the end date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date_lesser : int | None, optional
            Filter by the end date of the media.
            Must be an 8 digit long date integer (YYYYMMDD).
            Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500.
        end_date_like : str | None, optional
            Filter by the end date of the media.
        format_in : Iterable[MediaFormat] | None, optional
            Filter by the media's format.
        format_not : MediaFormat | None, optional
            Filter by the media's format.
        format_not_in : Iterable[MediaFormat] | None, optional
            Filter by the media's format.
        status_in : Iterable[MediaStatus] | None, optional
            Filter by the media's current release status.
        status_not : MediaStatus | None, optional
            Filter by the media's current release status.
        status_not_in : Iterable[MediaStatus] | None, optional
            Filter by the media's current release status.
        episodes_greater : int | None, optional
            Filter by amount of episodes the media has.
        episodes_lesser : int | None, optional
            Filter by amount of episodes the media has.
        duration_greater : int | None, optional
            Filter by the media's episode length.
        duration_lesser : int | None, optional
            Filter by the media's episode length.
        chapters_greater : int | None, optional
            Filter by the media's chapter count.
        chapters_lesser : int | None, optional
            Filter by the media's chapter count.
        volumes_greater : int | None, optional
            Filter by the media's volume count.
        volumes_lesser : int | None, optional
            Filter by the media's volume count.
        genre_in : Iterable[str] | None, optional
            Filter by the media's genres.
        genre_not_in : Iterable[str] | None, optional
            Filter by the media's genres.
        tag_in : Iterable[str] | None, optional
            Filter by the media's tags.
        tag_not_in : Iterable[str] | None, optional
            Filter by the media's tags.
        tag_category_in : Iterable[str] | None, optional
            Filter by the media's tags within a tag category.
        tag_category_not_in : Iterable[str] | None, optional
            Filter by the media's tags within a tag category.
        licensed_by_in : Iterable[str] | None, optional
            Filter media by sites name with a online streaming or reading license.
        licensed_by_id_in : Iterable[int] | None, optional
            Filter media by sites id with a online streaming or reading license.
        average_score_not : int | None, optional
            Filter by the media's average score.
        average_score_greater : int | None, optional
            Filter by the media's average score.
        average_score_lesser : int | None, optional
            Filter by the media's average score.
        popularity_not : int | None, optional
            Filter by the number of users with this media on their list.
        popularity_greater : int | None, optional
            Filter by the number of users with this media on their list.
        popularity_lesser : int | None, optional
            Filter by the number of users with this media on their list.
        source_in : Iterable[MediaSource] | None, optional
            Filter by the source type of the media.
        sort : SortType[MediaSort], optional
            The order the results will be returned in.
            Can be an instance of `MediaSort`, an iterable of `MediaSort`, or None.

        Raises
        ------
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        NoMediaArgumentsError
            If no media query arguments are provided.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        Yields
        ------
        Media
            An object representing the retrieved media.

        """

        # Collect and normalize the query variables
        variables = locals()
        variables.pop("self")
        variables = {to_anilist_case(key): value for key, value in variables.items() if value is not None}

        if not variables:
            raise NoMediaArgumentsError

        # We fetch four pages in one request with 50 results per page (AniList caps out at 50).
        variables["page1"] = 1
        variables["page2"] = 2
        variables["page3"] = 3
        variables["page4"] = 4
        variables["perPage"] = 50
        has_next_page: bool = True

        if sort_key := get_sort_key(sort, MediaSort):
            variables["sort"] = sort_key

        while has_next_page:
            response = await self._post(
                query=ALL_MEDIA_QUERY,
                variables=variables,
            )

            # As per Anilist's documentation:
            # "You should only rely on hasNextPage for any pagination logic."
            # Reference: https://docs.anilist.co/guide/graphql/pagination#pageinfo
            #
            # In our case, we are always grabbing 4 pages at a time,
            # so we only have to consider if there's any more pages
            # after the last page (page4)
            has_next_page = response["page4"]["pageInfo"]["hasNextPage"]

            if has_next_page:
                # Get the next set of 4 pages
                variables["page1"] += 4  # 1 + 4 => 5
                variables["page2"] += 4  # 2 + 4 => 6
                variables["page3"] += 4  # 3 + 4 => 7
                variables["page4"] += 4  # 4 + 4 => 8

            page1 = response["page1"]["media"]
            page2 = response["page2"]["media"]
            page3 = response["page3"]["media"]
            page4 = response["page4"]["media"]

            for media in itertools.chain(page1, page2, page3, page4):
                node: dict[str, Any] = normalize_anilist_data(media)
                if node:
                    # This check is necessary because in some cases,
                    # we may end up with an empty dictionary after normalizing.
                    # See: https://github.com/Ravencentric/pyanilist/issues/29
                    yield msgspec.convert(node, type=Media, strict=False)

    async def get_recommendations(
        self, media: MediaID, *, sort: SortType[RecommendationSort] = None
    ) -> AsyncIterator[Media]:
        """
        Retrieve recommended media based on a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get recommendations for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : SortType[RecommendationSort], optional
            Sorting criteria for the recommendations.
            Can be an instance of `RecommendationSort`, an iterable of `RecommendationSort`, or None.

        Yields
        ------
        Media
            An object representing the retrieved media.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if sort_key := get_sort_key(sort, RecommendationSort):
            variables["sort"] = sort_key

        response = await self._post(query=RECOMMENDATIONS_QUERY, variables=variables)
        recs = response["Media"]["recommendations"]["nodes"]

        for rec in recs:
            node: dict[str, Any] = normalize_anilist_data(rec["mediaRecommendation"])
            if node:
                # This check is necessary because in some cases,
                # we may end up with an empty dictionary after normalizing.
                # See: https://github.com/Ravencentric/pyanilist/issues/29
                yield msgspec.convert(node, type=Media, strict=False)

    async def get_relations(self, media: MediaID) -> AsyncIterator[RelatedMedia]:
        """
        Retrieve related media based on a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get relations for. Can be an ID (`int`), a URL (`str`), or a `Media` object.

        Yields
        ------
        RelatedMedia
            An object representing the retrieved related media.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        response = await self._post(query=RELATIONS_QUERY, variables={"mediaId": resolve_media_id(media)})
        relations = response["Media"]["relations"]["edges"]

        for relation in relations:
            node: dict[str, Any] = normalize_anilist_data(
                {"relationType": relation["relationType"], **relation["node"]}
            )
            if node:
                # This check is necessary because in some cases,
                # we may end up with an empty dictionary after normalizing.
                # See: https://github.com/Ravencentric/pyanilist/issues/29
                yield msgspec.convert(node, type=RelatedMedia, strict=False)

    async def get_studios(
        self,
        media: MediaID,
        *,
        sort: SortType[StudioSort] = None,
        is_main: bool | None = None,
    ) -> AsyncIterator[Studio]:
        """
        Retrieve studios based on a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get studios for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : SortType[StudioSort], optional
            Sorting criteria for the studios.
            Can be an instance of `StudioSort`, an iterable of `StudioSort`, or None.
        is_main : bool | None, optional
            Filter for the main studios (`True`), non-main studios (`False`), or all (`None`).

        Yields
        ------
        Studio
            An object representing the retrieved studio.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if sort_key := get_sort_key(sort, StudioSort):
            variables["sort"] = sort_key

        if is_main is not None:
            variables["isMain"] = is_main

        response = await self._post(query=STUDIOS_QUERY, variables=variables)
        studios = response["Media"]["studios"]["edges"]

        for studio in studios:
            node: dict[str, Any] = normalize_anilist_data({"isMain": studio["isMain"], **studio["node"]})
            if node:
                # This check is necessary because in some cases,
                # we may end up with an empty dictionary after normalizing.
                # See: https://github.com/Ravencentric/pyanilist/issues/29
                yield msgspec.convert(node, type=Studio, strict=False)

    async def get_staffs(
        self,
        media: MediaID,
        *,
        sort: SortType[StaffSort] = None,
    ) -> AsyncIterator[Staff]:
        """
        Retrieve staffs based on a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get staffs for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : SortType[StaffSort], optional
            Sorting criteria for the staffs.
            Can be an instance of `StaffSort`, an iterable of `StaffSort`, or None.

        Yields
        ------
        Staff
            An object representing the retrieved staff.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if sort_key := get_sort_key(sort, StaffSort):
            variables["sort"] = sort_key

        response = await self._post(query=STAFFS_QUERY, variables=variables)
        staffs = response["Media"]["staff"]["edges"]

        for staff in staffs:
            node = normalize_anilist_data({"role": staff["role"], **staff["node"]})
            if node:
                # This check is necessary because in some cases,
                # we may end up with an empty dictionary after normalizing.
                # See: https://github.com/Ravencentric/pyanilist/issues/29
                yield msgspec.convert(node, type=Staff, strict=False)

    async def get_airing_schedule(
        self,
        media: MediaID,
        *,
        not_yet_aired: bool | None = None,
    ) -> AsyncIterator[AiringSchedule]:
        """
        Retrieve the airing schedule for a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get the airing schedule for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        not_yet_aired : bool | None, optional
            Filter results to only include episodes that have not yet aired (`True`),
            exclude unaired episodes (`False`), or include all episodes (`None`).

        Yields
        ------
        AiringSchedule
            An object representing the retrieved airing schedule.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if not_yet_aired is not None:
            variables["notYetAired"] = not_yet_aired

        response = await self._post(query=AIRING_SCHEDULE_QUERY, variables=variables)
        schedules: list[dict[str, Any]] = normalize_anilist_data(response["Media"]["airingSchedule"]["nodes"])

        for schedule in schedules:
            yield msgspec.convert(schedule, type=AiringSchedule, strict=False)

    async def get_characters(
        self,
        media: MediaID,
        *,
        sort: SortType[CharacterSort] = None,
        role: CharacterRole | None = None,
    ) -> AsyncIterator[Character]:
        """
        Retrieve characters associated with a given `Media` object or ID.

        Parameters
        ----------
        media : MediaID
            The media to get characters for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : SortType[CharacterSort], optional
            Sorting criteria for the characters.
            Can be an instance of `CharacterSort`, an iterable of `CharacterSort`, or None.
        role : CharacterRole | None, optional
            Filter characters by their role in the media. If `None`, no filtering is applied.

        Yields
        ------
        Character
            An object representing the retrieved character.

        Raises
        ------
        MediaNotFoundError
            If the provided `media` ID or URL does not correspond to any existing media on Anilist.
        RateLimitError
            If the API rate limit is exceeded. The error will contain information on how long to wait before retrying.
        AnilistError
            If any other error occurs during the API request.
        TypeError
            If `media` or `sort` are not of the expected type.
        ValueError
            If the provided `media` URL is invalid.

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if sort_key := get_sort_key(sort, CharacterSort):
            variables["sort"] = sort_key

        if role is not None:
            variables["role"] = role

        response = await self._post(query=CHARACTERS_QUERY, variables=variables)
        characters = response["Media"]["characters"]["edges"]

        for character in characters:
            node: dict[str, Any] = normalize_anilist_data(
                {"role": character["role"], "voiceActors": character["voiceActors"], **character["node"]}
            )
            if node:
                # This check is necessary because in some cases,
                # we may end up with an empty dictionary after normalizing.
                # See: https://github.com/Ravencentric/pyanilist/issues/29
                yield msgspec.convert(node, type=Character, strict=False)
