from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, TypeVar, Union

if TYPE_CHECKING:
    from typing_extensions import Self

import msgspec

from pyanilist._enums import (
    CharacterRole,
    ExternalLinkType,
    MediaFormat,
    MediaRankType,
    MediaRelation,
    MediaSeason,
    MediaSource,
    MediaStatus,
    MediaType,
)

# -------------------- TYPE ALIASES --------------------

T = TypeVar("T")

SortType: TypeAlias = Iterable[T] | T | None
"""
Represents the structure for AniList's sort parameter.
It can be a single sort key, an iterable of sort keys, or None.
"""

MediaID: TypeAlias = Union[int, str, "Media"]
"""
Represents the different ways to identify media items.
Can be an integer ID, a string URL, or a [`Media`][pyanilist.Media] object.
"""

# -------------------- REAL ANILIST TYPES (CLASSES) --------------------


class Base(
    msgspec.Struct,
    forbid_unknown_fields=True,
    repr_omit_defaults=True,
    frozen=True,
    kw_only=True,
):
    """Base class for AniList data structures."""

    @classmethod
    def from_dict(cls, data: dict[str, Any], /) -> Self:
        """
        Create an instance of this class from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        return msgspec.convert(data, type=cls)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the instance of this class into a dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representing the instance of this class.

        """
        return msgspec.to_builtins(self)  # type: ignore[no-any-return]

    @classmethod
    def from_json(cls, data: str | bytes, /) -> Self:
        """
        Create an instance of this class from JSON data.

        Parameters
        ----------
        data : str | bytes
            JSON data representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        return msgspec.json.decode(data, type=cls)

    def to_json(self, *, indent: int = 2) -> str:
        """
        Serialize the instance of this class into a JSON string.

        Parameters
        ----------
        indent : int, optional
            Number of spaces for indentation.
            Set to 0 for a single line with spacing,
            or negative to minimize size by removing extra whitespace.

        Returns
        -------
        str
            JSON string representing this class.

        """
        jsonified = msgspec.json.encode(self)
        return msgspec.json.format(jsonified, indent=indent).decode()


class MediaTitle(Base, frozen=True, kw_only=True):
    """The official titles of the media in various languages."""

    romaji: str | None = None
    """The romanization of the native language title."""

    english: str | None = None
    """The official English title."""

    native: str | None = None
    """Official title in its native language."""

    def to_str(self) -> str:
        """
        Return the media title as a string in the following order of preference:
        English, Romaji, or native.
        """
        return self.english or self.romaji or self.native  # type: ignore[return-value]

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class FuzzyDate(Base, frozen=True, kw_only=True):
    """Naive date object that allows for incomplete date values (fuzzy)."""

    year: int | None = None
    """Numeric Year (2017)."""

    month: int | None = None
    """Numeric Month (3)."""

    day: int | None = None
    """Numeric Day (24)."""

    def iso_format(self) -> str:
        """
        Return the date formatted as an ISO 8601 string.

        If year, month, and day are available, the format is "YYYY-MM-DD".
        If only year and month are available, the format is "YYYY-MM".
        If only year is available, the format is "YYYY".
        If no information is available, an empty string is returned.
        """
        if self.year and self.month and self.day:
            return f"{self.year}-{self.month:02}-{self.day:02}"

        if self.year and self.month:
            return f"{self.year}-{self.month:02}"

        if self.year:
            return f"{self.year}"

        return ""

    def to_int(self) -> int:
        """
        Return an 8 digit long date integer (YYYYMMDD).
        Unknown dates represented by 0.
        For example, 2016 is 20160000 and May 1976 is 19760500.
        """
        year = str(self.year).zfill(4) if self.year is not None else "1000"
        month = str(self.month).zfill(2) if self.month is not None else "00"
        day = str(self.day).zfill(2) if self.day is not None else "00"

        return int(f"{year}{month}{day}")

    def __str__(self) -> str:
        """Stringify. Identical to `iso_format()`."""
        return self.iso_format()

    def __int__(self) -> int:
        """Support `int(FuzzyDate())`. Identical to `to_int()`."""
        return self.to_int()


class MediaTrailer(Base, frozen=True, kw_only=True):
    """Media trailer or advertisement."""

    id: str | None = None
    """The trailer video id."""

    site: str | None = None
    """The site the video is hosted by (Currently either youtube or dailymotion)."""

    thumbnail: str | None = None
    """The url for the thumbnail image of the video."""


class MediaCoverImage(Base, frozen=True, kw_only=True):
    """The cover images of the media."""

    extra_large: str | None = None
    """
    The cover image url of the media at its largest size.
    If this size isn't available, large will be provided instead.
    """

    large: str | None = None
    """The cover image url of the media at a large size"""

    medium: str | None = None
    """The cover image url of the media at medium size"""

    color: str | None = None
    """Average #hex color of cover image"""

    def to_str(self) -> str:
        """
        Return the media cover image URL as a string in the following order of preference:
        Extra Large, Large, or Medium.
        """
        return str(self.extra_large or self.large or self.medium or "")

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class MediaTag(Base, frozen=True, kw_only=True):
    """A tag that describes a theme or element of the media."""

    id: int | None = None
    """The id of the tag."""

    name: str | None = None
    """The name of the tag."""

    description: str | None = None
    """A general description of the tag."""

    category: str | None = None
    """The categories of tags this tag belongs to."""

    rank: int | None = None
    """The relevance ranking of the tag out of the 100 for this media."""

    is_general_spoiler: bool | None = None
    """If the tag could be a spoiler for any media."""

    is_media_spoiler: bool | None = None
    """If the tag is a spoiler for this media."""

    is_adult: bool | None = None
    """If the tag is only for adult 18+ media."""

    user_id: int | None = None
    """The user who submitted the tag."""


class AiringSchedule(Base, frozen=True, kw_only=True):
    """Media Airing Schedule."""

    id: int | None = None
    """The id of the airing schedule item."""

    airing_at: datetime | None = None
    """The time the episode airs at."""

    time_until_airing: timedelta | None = None
    """The time delta until the episode starts airing."""

    episode: int | None = None
    """The airing episode number."""


class MediaExternalLink(Base, frozen=True, kw_only=True):
    """An external link to another site related to the media or staff member."""

    id: int | None = None
    """The id of the external link."""

    url: str | None = None
    """The url of the external link or base url of link source."""

    site: str | None = None
    """The links website site name."""

    site_id: int | None = None
    """The links website site id."""

    type: ExternalLinkType | None = None
    """Type of the external link."""

    language: str | None = None
    """Language the site content is in. See Staff language field for values."""

    color: str | None = None
    """Average #hex color."""

    icon: str | None = None
    """The icon image url of the site. Not available for all links. Transparent PNG 64x64."""

    notes: str | None = None
    """Additional notes about the link or its relevance."""

    is_disabled: bool | None = None
    """Indicates if the link is currently disabled."""


class MediaStreamingEpisode(Base, frozen=True, kw_only=True):
    """Data and links to legal streaming episodes on external sites."""

    title: str | None = None
    """Title of the episode."""

    thumbnail: str | None = None
    """Url of episode image thumbnail."""

    url: str | None = None
    """The url of the episode."""

    site: str | None = None
    """The site location of the streaming episodes."""


class Studio(Base, frozen=True, kw_only=True):
    """Animation or production company."""

    id: int | None = None
    """The id of the studio."""

    name: str | None = None
    """The name of the studio."""

    is_animation_studio: bool | None = None
    """If the studio is an animation studio or a different kind of company."""

    site_url: str | None = None
    """The url for the studio page on the AniList website."""

    favourites: int | None = None
    """The amount of user's who have favourited the studio."""

    is_main: bool | None = None
    """If the studio is the main animation studio of the anime."""


class StaffName(Base, frozen=True, kw_only=True):
    """The names of the staff member."""

    first: str | None = None
    """The person's given name."""

    middle: str | None = None
    """The person's middle name."""

    last: str | None = None
    """The person's surname."""

    full: str | None = None
    """The person's first and last name."""

    native: str | None = None
    """The person's full name in their native language."""

    alternative: tuple[str, ...] = ()
    """Other names the staff member might be referred to as (pen names)."""

    def to_str(self) -> str:
        """
        Return the staff name as a string in the following order of preference:
        Full, First, or Native.
        """
        return self.full or self.first or self.native or ""

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class StaffImage(Base, frozen=True, kw_only=True):
    """Staff's image."""

    large: str | None = None
    """The person's image of media at its largest size."""

    medium: str | None = None
    """The person's image of media at medium size."""

    def to_str(self) -> str:
        """
        Return the staff image URL as a string in the following order of preference:
        Large or Medium.
        """
        return str(self.large or self.medium or "")

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    [`Staff.years_active`][pyanilist.Staff.years_active].
    """

    start_year: int | None = None
    end_year: int | None = None


class Staff(Base, frozen=True, kw_only=True):
    """Voice actors or production staff."""

    id: int | None = None
    """The id of the staff member."""

    name: StaffName | None = None
    """The names of the staff member."""

    language_v2: str | None = None
    """
    The primary language of the staff member.
    Current values: Japanese, English, Korean,
    Italian, Spanish, Portuguese, French, German,
    Hebrew, Hungarian, Chinese, Arabic, Filipino,
    Catalan, Finnish, Turkish, Dutch, Swedish, Thai,
    Tagalog, Malaysian, Indonesian, Vietnamese, Nepali,
    Hindi, Urdu.
    """

    image: StaffImage | None = None
    """The staff images."""

    description: str | None = None
    """A general description of the staff member."""

    primary_occupations: tuple[str, ...] = ()
    """The person's primary occupations."""

    gender: str | None = None
    """The staff's gender. Usually Male, Female, or Non-binary but can be any string."""

    date_of_birth: FuzzyDate | None = None
    """The staff's date of birth."""

    date_of_death: FuzzyDate | None = None
    """The staff's date of death."""

    age: int | None = None
    """The person's age in years."""

    years_active: YearsActive | None = None
    """(start_year, end_year) (If the 2nd value is not present staff is still active)."""

    home_town: str | None = None
    """The persons birthplace or hometown."""

    blood_type: str | None = None
    """The persons blood type."""

    site_url: str | None = None
    """The url for the staff page on the AniList website."""

    role: str | None = None
    """The role of the staff member in the production of the media."""

    favourites: int | None = None
    """The amount of user's who have favourited the staff member."""


class CharacterName(Base, frozen=True, kw_only=True):
    """The names of the character."""

    first: str | None = None
    """The character's given name."""

    middle: str | None = None
    """The character's middle name."""

    last: str | None = None
    """The character's surname."""

    full: str | None = None
    """The character's first and last name."""

    native: str | None = None
    """The character's full name in their native language."""

    alternative: tuple[str, ...] = ()
    """Other names the character might be referred to as."""

    alternative_spoiler: tuple[str, ...] = ()
    """Other names the character might be referred to as but are spoilers."""

    def to_str(self) -> str:
        """
        Return the character name as a string in the following order of preference:
        Full, First, or Native.
        """
        return self.full or self.first or self.native or ""

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class CharacterImage(Base, frozen=True, kw_only=True):
    """Character's image."""

    large: str | None = None
    """The character's image of media at its largest size."""

    medium: str | None = None
    """The character's image of media at medium size."""

    def to_str(self) -> str:
        """
        Return the character image URL as a string in the following order of preference:
        Large or Medium.
        """
        return str(self.large or self.medium or "")

    def __str__(self) -> str:
        """Stringify. Identical to `to_str()`."""
        return self.to_str()


class Character(Base, frozen=True, kw_only=True):
    """A character that features in an anime or manga."""

    id: int
    """The id of the character."""

    name: CharacterName | None = None
    """The names of the character."""

    image: CharacterImage | None = None
    """Character images."""

    description: str | None = None
    """A general description of the character."""

    gender: str | None = None
    """The character's gender. Usually Male, Female, or Non-binary but can be any string."""

    date_of_birth: FuzzyDate | None = None
    """The character's birth date."""

    age: str | None = None
    """The character's age. Note this is a string, not an int, it may contain further text and additional ages."""

    blood_type: str | None = None
    """The character's blood type."""

    site_url: str | None = None
    """The url for the character page on the AniList website."""

    favourites: int | None = None
    """The amount of user's who have favourited the character."""

    role: CharacterRole | None = None
    """The character's role in the media."""

    voice_actors: tuple[Staff, ...] = ()
    """The voice actors of the character."""


class MediaRank(Base, frozen=True, kw_only=True):
    """The ranking of a media in a particular time span and format compared to other media."""

    id: int | None = None
    """The id of the rank."""

    rank: int | None = None
    """The numerical rank of the media."""

    type: MediaRankType | None = None
    """The type of ranking."""

    format: MediaFormat | None = None
    """The format the media is ranked within."""

    year: int | None = None
    """The year the media is ranked within."""

    season: MediaSeason | None = None
    """The season the media is ranked within."""

    all_time: bool | None = None
    """If the ranking is based on all time instead of a season/year."""

    context: str | None = None
    """String that gives context to the ranking type and time span."""


class Media(Base, frozen=True, kw_only=True):
    """Anime or Manga."""

    id: int
    """The id of the media."""

    id_mal: int | None = None
    """The mal id of the media."""

    type: MediaType | None = None
    """The type of the media; anime or manga."""

    format: MediaFormat | None = None
    """The format the media was released in."""

    status: MediaStatus | None = None
    """The current releasing status of the media."""

    description: str | None = None
    """Short description of the media's story and characters."""

    season: MediaSeason | None = None
    """The season the media was initially released in."""

    season_year: int | None = None
    """The season year the media was initially released in."""

    episodes: int | None = None
    """The amount of episodes the anime has when complete."""

    duration: int | None = None
    """The general length of each anime episode in minutes."""

    chapters: int | None = None
    """The amount of chapters the manga has when complete."""

    volumes: int | None = None
    """The amount of volumes the manga has when complete."""

    country_of_origin: str | None = None
    """Where the media was created. (ISO 3166-1 alpha-2)."""

    is_licensed: bool | None = None
    """If the media is officially licensed or a self-published doujin release."""

    source: MediaSource | None = None
    """Source type the media was adapted from."""

    hashtag: str | None = None
    """Official Twitter hashtags for the media."""

    updated_at: datetime | None = None
    """When the media's data was last updated."""

    banner_image: str | None = None
    """The banner image of the media."""

    genres: tuple[str, ...] = ()
    """The genres of the media."""

    synonyms: tuple[str, ...] = ()
    """Alternative titles of the media."""

    average_score: int | None = None
    """A weighted average score of all the user's scores of the media."""

    mean_score: int | None = None
    """Mean score of all the user's scores of the media."""

    popularity: int | None = None
    """The number of users with the media on their list."""

    is_locked: bool | None = None
    """
    Locked media may not be added to lists or favorited.
    This may be due to the entry pending for deletion or other reasons.
    """

    trending: int | None = None
    """The amount of related activity in the past hour."""

    favourites: int | None = None
    """The amount of user's who have favourited the media."""

    is_adult: bool | None = None
    """If the media is intended only for 18+ adult audiences."""

    site_url: str
    """The url for the media page on the AniList website."""

    trailer: MediaTrailer | None = None
    """Media trailer or advertisement."""

    title: MediaTitle
    """The official titles of the media in various languages."""

    tags: tuple[MediaTag, ...] = ()
    """List of tags that describes elements and themes of the media."""

    start_date: FuzzyDate | None = None
    """The first official release date of the media."""

    rankings: tuple[MediaRank, ...] = ()
    """The ranking of the media in a particular time span and format compared to other media."""

    external_links: tuple[MediaExternalLink, ...] = ()
    """External links to another site related to the media."""

    end_date: FuzzyDate | None = None
    """The last official release date of the media."""

    cover_image: MediaCoverImage | None = None
    """The cover images of the media."""

    next_airing_episode: AiringSchedule | None = None
    """The media's next episode airing schedule."""

    streaming_episodes: tuple[MediaStreamingEpisode, ...] = ()
    """Data and links to legal streaming episodes on external sites."""


class RelatedMedia(Media, frozen=True, kw_only=True):
    """Subclass of `Media` with an additional `relation_type` property."""

    relation_type: MediaRelation | None = None
    """The type of relation to the parent media."""
