from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any

from httpx import Client
from typing_extensions import Self, assert_never

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
from pyanilist._models import AiringSchedule, Character, Media, RelatedMedia, Staff, Studio
from pyanilist._query import (
    AIRING_SCHEDULE_QUERY,
    CHARACTERS_QUERY,
    MEDIA_QUERY,
    RECOMMENDATIONS_QUERY,
    RELATIONS_QUERY,
    STAFFS_QUERY,
    STUDIOS_QUERY,
)
from pyanilist._utils import remove_null_fields, resolve_media_id, to_anilist_case
from pyanilist._version import __version__


class AniList:
    def __init__(self, api_url: str = "https://graphql.anilist.co", *, client: Client | None = None) -> None:
        """
        AniList API client.

        Parameters
        ----------
        api_url : str, optional
            The URL of the AniList API.
        client : Client | None, optional
            An [`httpx.Client`](https://www.python-httpx.org/api/#client) instance used to make requests to AniList.

        """
        self._api_url = api_url
        self._client = (
            Client(headers={"Referer": "https://anilist.co", "user-agent": f"pyanilist/{__version__}"})
            if client is None
            else client
        )

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def _post(self, *, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Utiliy function to POST to Anilist."""
        response = self._client.post(self._api_url, json=dict(query=query, variables=variables))
        return response.raise_for_status().json()["data"]["Media"]  # type: ignore[no-any-return]

    def get_media(
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
        sort: Iterable[MediaSort] | None = None,
    ) -> Media:
        """
        Search for media on AniList based on the provided parameters.

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
        sort : Iterable[MediaSort] | None, optional
            The order the results will be returned in.

        Raises
        ------
        HTTPStatusError
            AniList returned a non 2xx response.

        Returns
        -------
        Media
            A Media object representing the retrieved media information.

        """

        variables = locals()
        variables.pop("self")

        media = self._post(
            query=MEDIA_QUERY,
            variables={to_anilist_case(key): value for key, value in variables.items() if value is not None},
        )

        return Media.model_validate(remove_null_fields(media))

    def get_recommendations(
        self, media: int | str | Media, *, sort: Iterable[RecommendationSort] | RecommendationSort | None = None
    ) -> Iterator[Media]:
        """
        Retrieve recommended media based on a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get recommendations for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : Iterable[RecommendationSort] | RecommendationSort | None, optional
            Sorting criteria for the recommendations.

        Yields
        ------
        Media

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        match sort:  # pragma: no cover
            case RecommendationSort():
                variables["sort"] = [sort]
            case Iterable():
                variables["sort"] = sort
            case None:
                pass
            case _:
                assert_never(sort)

        recs = self._post(query=RECOMMENDATIONS_QUERY, variables=variables)["recommendations"]["nodes"]

        for rec in recs:
            yield self.get_media(id=int(rec["mediaRecommendation"]["id"]))

    def get_relations(self, media: int | str | Media) -> Iterator[RelatedMedia]:
        """
        Retrieve related media based on a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get relations for. Can be an ID (`int`), a URL (`str`), or a `Media` object.

        Yields
        ------
        RelatedMedia

        """
        relations = self._post(query=RELATIONS_QUERY, variables={"mediaId": resolve_media_id(media)})["relations"][
            "edges"
        ]

        for relation in relations:
            relation_type = relation["relationType"]
            media_id = int(relation["node"]["id"])
            media = self.get_media(id=media_id)

            yield RelatedMedia(relation_type=relation_type, **media.model_dump())

    def get_studios(
        self,
        media: int | str | Media,
        *,
        sort: Iterable[StudioSort] | StudioSort | None = None,
        is_main: bool | None = None,
    ) -> Iterator[Studio]:
        """
        Retrieve studios based on a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get studios for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : Iterable[StudioSort] | StudioSort | None, optional
            Sorting criteria for the studios.
        is_main : bool | None, optional
            Filter for the main studios (`True`), non-main studios (`False`), or all (`None`).

        Yields
        ------
        Studio

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        match sort:  # pragma: no cover
            case StudioSort():
                variables["sort"] = [sort]
            case Iterable():
                variables["sort"] = sort
            case None:
                pass
            case _:
                assert_never(sort)

        if is_main is not None:  # pragma: no cover
            variables["isMain"] = is_main

        studios = self._post(query=STUDIOS_QUERY, variables=variables)["studios"]["edges"]

        for studio in studios:
            yield Studio.model_validate({"isMain": studio["isMain"], **studio["node"]})

    def get_staffs(
        self,
        media: int | str | Media,
        *,
        sort: Iterable[StaffSort] | StaffSort | None = None,
    ) -> Iterator[Staff]:
        """
        Retrieve staffs based on a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get staffs for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : Iterable[StaffSort] | StaffSort | None, optional
            Sorting criteria for the staffs.

        Yields
        ------
        Staff

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        match sort:  # pragma: no cover
            case StaffSort():
                variables["sort"] = [sort]
            case Iterable():
                variables["sort"] = sort
            case None:
                pass
            case _:
                assert_never(sort)

        staffs = self._post(query=STAFFS_QUERY, variables=variables)["staff"]["edges"]

        for staff in staffs:
            yield Staff.model_validate({"role": staff["role"], **staff["node"]})

    def get_airing_schedule(
        self,
        media: int | str | Media,
        *,
        not_yet_aired: bool | None = None,
    ) -> Iterator[AiringSchedule]:
        """
        Retrieve the airing schedule for a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get the airing schedule for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        not_yet_aired : bool | None, optional
            Filter results to only include episodes that have not yet aired (`True`),
            exclude unaired episodes (`False`), or include all episodes (`None`).

        Yields
        ------
        AiringSchedule

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        if not_yet_aired is not None:  # pragma: no cover
            variables["notYetAired"] = not_yet_aired

        schedules = self._post(query=AIRING_SCHEDULE_QUERY, variables=variables)["airingSchedule"]["nodes"]

        for schedule in schedules:
            yield AiringSchedule.model_validate(schedule)

    def get_characters(
        self,
        media: int | str | Media,
        *,
        sort: Iterable[CharacterSort] | CharacterSort | None = None,
        role: CharacterRole | None = None,
    ) -> Iterator[Character]:
        """
        Retrieve characters associated with a given `Media` object or ID.

        Parameters
        ----------
        media : int | str | Media
            The media to get characters for. Can be an ID (`int`), a URL (`str`), or a `Media` object.
        sort : Iterable[CharacterSort] | CharacterSort | None, optional
            Sorting criteria for the characters.
        role : CharacterRole | None, optional
            Filter characters by their role in the media. If `None`, no filtering is applied.

        Yields
        ------
        Character

        """
        variables: dict[str, Any] = {"mediaId": resolve_media_id(media)}

        match sort:  # pragma: no cover
            case CharacterSort():
                variables["sort"] = [sort]
            case Iterable():
                variables["sort"] = sort
            case None:
                pass
            case _:
                assert_never(sort)

        if role is not None:  # pragma: no cover
            variables["role"] = role

        characters = self._post(query=CHARACTERS_QUERY, variables=variables)["characters"]["edges"]

        for character in characters:
            yield Character.model_validate(
                {"role": character["role"], "voiceActors": character["voiceActors"], **character["node"]}
            )
