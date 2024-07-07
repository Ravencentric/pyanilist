from __future__ import annotations

from typing import Any

from httpx import AsyncClient, HTTPError, Response
from pydantic import PositiveInt, validate_call
from stamina import retry_context

from .._enums import MediaFormat, MediaSeason, MediaSort, MediaSource, MediaStatus, MediaType
from .._models import Media
from .._parser import post_process_response
from .._query import query_string
from .._types import CollectionOf, FuzzyDateInt
from .._utils import to_anilist_case


class AsyncAniList:
    @validate_call
    def __init__(self, api_url: str = "https://graphql.anilist.co", retries: PositiveInt = 5, **kwargs: Any) -> None:
        """
        AniList API client.

        Parameters
        ----------
        api_url : str, optional
            The URL of the AniList API. Default is `https://graphql.anilist.co`.
        retries : PositiveInt, optional
            Number of times to retry a failed request before raising an error. Default is 5.
            Set this to 1 to disable retrying.
        kwargs : Any, optional
            Keyword arguments to pass to the underlying [`httpx.AsyncClient`](https://www.python-httpx.org/api/#asyncclient)
            used to make the POST request.
        """
        self.api_url = api_url
        self.retries = retries
        self.kwargs = kwargs

    async def _post_request(self, **kwargs: Any) -> Response:
        """
        Make a POST request to the AniList API.

        Parameters
        ----------
        kwargs : Any
            Anilist query kwargs

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

        payload = {
            "query": query_string,
            "variables": {to_anilist_case(key): value for key, value in kwargs.items() if value is not None},
        }

        async for attempt in retry_context(on=HTTPError, attempts=self.retries):
            with attempt:
                async with AsyncClient(**self.kwargs) as client:
                    response = await client.post(self.api_url, json=payload)
                    response.raise_for_status()

        return response

    @validate_call
    async def get(
        self,
        search: str | None = None,
        *,
        id: int | None = None,
        id_mal: int | None = None,
        start_date: FuzzyDateInt | None = None,
        end_date: FuzzyDateInt | None = None,
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
        id_in: CollectionOf[int] | None = None,
        id_not_in: CollectionOf[int] | None = None,
        id_mal_not: int | None = None,
        id_mal_in: CollectionOf[int] | None = None,
        id_mal_not_in: CollectionOf[int] | None = None,
        start_date_greater: FuzzyDateInt | None = None,
        start_date_lesser: FuzzyDateInt | None = None,
        start_date_like: str | None = None,
        end_date_greater: FuzzyDateInt | None = None,
        end_date_lesser: FuzzyDateInt | None = None,
        end_date_like: str | None = None,
        format_in: CollectionOf[MediaFormat] | None = None,
        format_not: MediaFormat | None = None,
        format_not_in: CollectionOf[MediaFormat] | None = None,
        status_in: CollectionOf[MediaStatus] | None = None,
        status_not: MediaStatus | None = None,
        status_not_in: CollectionOf[MediaStatus] | None = None,
        episodes_greater: int | None = None,
        episodes_lesser: int | None = None,
        duration_greater: int | None = None,
        duration_lesser: int | None = None,
        chapters_greater: int | None = None,
        chapters_lesser: int | None = None,
        volumes_greater: int | None = None,
        volumes_lesser: int | None = None,
        genre_in: CollectionOf[str] | None = None,
        genre_not_in: CollectionOf[str] | None = None,
        tag_in: CollectionOf[str] | None = None,
        tag_not_in: CollectionOf[str] | None = None,
        tag_category_in: CollectionOf[str] | None = None,
        tag_category_not_in: CollectionOf[str] | None = None,
        licensed_by_in: CollectionOf[str] | None = None,
        licensed_by_id_in: CollectionOf[int] | None = None,
        average_score_not: int | None = None,
        average_score_greater: int | None = None,
        average_score_lesser: int | None = None,
        popularity_not: int | None = None,
        popularity_greater: int | None = None,
        popularity_lesser: int | None = None,
        source_in: CollectionOf[MediaSource] | None = None,
        sort: CollectionOf[MediaSort] | None = None,
    ) -> Media:
        """
        Search for media on AniList based on the provided parameters.

        Parameters
        ----------
        search : str, optional
            Filter by search query
        id : int, optional
            Filter by the media id
        id_mal : int, optional
            Filter by the media's MyAnimeList id
        start_date : FuzzyDateInt, optional
            Filter by the start date of the media
        end_date : FuzzyDateInt, optional
            Filter by the end date of the media
        season : MediaSeason, optional
            Filter by the season the media was released in
        season_year : int, optional
            The year of the season (Winter 2017 would also include December 2016 releases). Requires season argument
        type : MediaType, optional
            Filter by the media's type
        format : MediaFormat, optional
            Filter by the media's format
        status : MediaStatus, optional
            Filter by the media's current release status
        episodes : int, optional
            Filter by amount of episodes the media has
        chapters : int, optional
            Filter by the media's episode length
        duration : int, optional
            Filter by the media's chapter count
        volumes : int, optional
            Filter by the media's volume count
        is_adult : bool, optional
            Filter by if the media's intended for 18+ adult audiences
        genre : str, optional
            Filter by the media's genres
        tag : str, optional
            Filter by the media's tags
        minimum_tag_rank : int, optional
            Only apply the tags filter argument to tags above this rank. Default: 18
        tag_category : str, optional
            Filter by the media's tags within a tag category
        licensed_by : str, optional
            Filter media by sites name with a online streaming or reading license
        licensed_by_id : int, optional
            Filter media by sites id with a online streaming or reading license
        average_score : int, optional
            Filter by the media's average score
        popularity : int, optional
            Filter by the number of users with this media on their list
        source : MediaSource, optional
            Filter by the source type of the media
        country_of_origin : str, optional
            Filter by the media's country of origin
        is_licensed : bool, optional
            If the media is officially licensed or a self-published doujin release
        id_not : int, optional
            Filter by the media id
        id_in : CollectionOf[int], optional
            Filter by the media id
        id_not_in : CollectionOf[int], optional
            Filter by the media id
        id_mal_not : int, optional
            Filter by the media's MyAnimeList id
        id_mal_in : CollectionOf[int], optional
            Filter by the media's MyAnimeList id
        id_mal_not_in : CollectionOf[int], optional
            Filter by the media's MyAnimeList id
        start_date_greater : FuzzyDateInt, optional
            Filter by the start date of the media
        start_date_lesser : FuzzyDateInt, optional
            Filter by the start date of the media
        start_date_like : str, optional
            Filter by the start date of the media
        end_date_greater : FuzzyDateInt, optional
            Filter by the end date of the media
        end_date_lesser : FuzzyDateInt, optional
            Filter by the end date of the media
        end_date_like : str, optional
            Filter by the end date of the media
        format_in : CollectionOf[MediaFormat], optional
            Filter by the media's format
        format_not : MediaFormat, optional
            Filter by the media's format
        format_not_in : CollectionOf[MediaFormat], optional
            Filter by the media's format
        status_in : CollectionOf[MediaStatus], optional
            Filter by the media's current release status
        status_not : MediaStatus, optional
            Filter by the media's current release status
        status_not_in : CollectionOf[MediaStatus], optional
            Filter by the media's current release status
        episodes_greater : int, optional
            Filter by amount of episodes the media has
        episodes_lesser : int, optional
            Filter by amount of episodes the media has
        duration_greater : int, optional
            Filter by the media's episode length
        duration_lesser : int, optional
            Filter by the media's episode length
        chapters_greater : int, optional
            Filter by the media's chapter count
        chapters_lesser : int, optional
            Filter by the media's chapter count
        volumes_greater : int, optional
            Filter by the media's volume count
        volumes_lesser : int, optional
            Filter by the media's volume count
        genre_in : CollectionOf[str], optional
            Filter by the media's genres
        genre_not_in : CollectionOf[str], optional
            Filter by the media's genres
        tag_in : CollectionOf[str], optional
            Filter by the media's tags
        tag_not_in : CollectionOf[str], optional
            Filter by the media's tags
        tag_category_in : CollectionOf[str], optional
            Filter by the media's tags within a tag category
        tag_category_not_in : CollectionOf[str], optional
            Filter by the media's tags within a tag category
        licensed_by_in : CollectionOf[str], optional
            Filter media by sites name with a online streaming or reading license
        licensed_by_id_in : CollectionOf[int], optional
            Filter media by sites id with a online streaming or reading license
        average_score_not : int, optional
            Filter by the media's average score
        average_score_greater : int, optional
            Filter by the media's average score
        average_score_lesser : int, optional
            Filter by the media's average score
        popularity_not : int, optional
            Filter by the number of users with this media on their list
        popularity_greater : int, optional
            Filter by the number of users with this media on their list
        popularity_lesser : int, optional
            Filter by the number of users with this media on their list
        source_in : CollectionOf[MediaSource], optional
            Filter by the source type of the media
        sort : CollectionOf[MediaSort], optional
            The order the results will be returned in

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
            post_process_response(
                await self._post_request(
                    id=id,
                    id_mal=id_mal,
                    start_date=start_date,
                    end_date=end_date,
                    season=season,
                    season_year=season_year,
                    type=type,
                    format=format,
                    status=status,
                    episodes=episodes,
                    chapters=chapters,
                    duration=duration,
                    volumes=volumes,
                    is_adult=is_adult,
                    genre=genre,
                    tag=tag,
                    minimum_tag_rank=minimum_tag_rank,
                    tag_category=tag_category,
                    licensed_by=licensed_by,
                    licensed_by_id=licensed_by_id,
                    average_score=average_score,
                    popularity=popularity,
                    source=source,
                    country_of_origin=country_of_origin,
                    is_licensed=is_licensed,
                    search=search,
                    id_not=id_not,
                    id_in=id_in,
                    id_not_in=id_not_in,
                    id_mal_not=id_mal_not,
                    id_mal_in=id_mal_in,
                    id_mal_not_in=id_mal_not_in,
                    start_date_greater=start_date_greater,
                    start_date_lesser=start_date_lesser,
                    start_date_like=start_date_like,
                    end_date_greater=end_date_greater,
                    end_date_lesser=end_date_lesser,
                    end_date_like=end_date_like,
                    format_in=format_in,
                    format_not=format_not,
                    format_not_in=format_not_in,
                    status_in=status_in,
                    status_not=status_not,
                    status_not_in=status_not_in,
                    episodes_greater=episodes_greater,
                    episodes_lesser=episodes_lesser,
                    duration_greater=duration_greater,
                    duration_lesser=duration_lesser,
                    chapters_greater=chapters_greater,
                    chapters_lesser=chapters_lesser,
                    volumes_greater=volumes_greater,
                    volumes_lesser=volumes_lesser,
                    genre_in=genre_in,
                    genre_not_in=genre_not_in,
                    tag_in=tag_in,
                    tag_not_in=tag_not_in,
                    tag_category_in=tag_category_in,
                    tag_category_not_in=tag_category_not_in,
                    licensed_by_in=licensed_by_in,
                    licensed_by_id_in=licensed_by_id_in,
                    average_score_not=average_score_not,
                    average_score_greater=average_score_greater,
                    average_score_lesser=average_score_lesser,
                    popularity_not=popularity_not,
                    popularity_greater=popularity_greater,
                    popularity_lesser=popularity_lesser,
                    source_in=source_in,
                    sort=sort,
                )
            )
        )
