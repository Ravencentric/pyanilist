from __future__ import annotations

from datetime import datetime

from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from ._enums import (
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
from ._types import Color, CountryCode, HttpUrl, YearsActive


class ParentModel(BaseModel):
    """
    Parent Model that stores the global configuration
    All models ahead will inherit from this
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            # Anilist uses camelCase
            alias=to_camel,
        ),
        frozen=True,
        populate_by_name=True,
    )


class MediaTitle(ParentModel):
    """The official titles of the media in various languages."""

    romaji: str | None = None
    """The romanization of the native language title"""

    english: str | None = None
    """The official English title"""

    native: str | None = None
    """Official title in its native language"""


class FuzzyDate(ParentModel):
    """Naive date object that allows for incomplete date values (fuzzy)."""

    year: int | None = None
    """Numeric Year (2017)"""

    month: int | None = None
    """Numeric Month (3)"""

    day: int | None = None
    """Numeric Day (24)"""

    def iso_format(self) -> str:
        """
        Returns the date formatted as an ISO 8601 string.

        If year, month, and day are available, the format is "YYYY-MM-DD".
        If only year and month are available, the format is "YYYY-MM".
        If only year is available, the format is "YYYY".
        If no information is available, an empty string is returned.
        """
        if self.year and self.month and self.day:
            return f"{self.year}-{self.month:02}-{self.day:02}"

        elif self.year and self.month:
            return f"{self.year}-{self.month:02}"

        elif self.year:
            return f"{self.year}"

        else:
            return ""


class MediaTrailer(ParentModel):
    """Media trailer or advertisement."""

    id: str | None = None
    """The trailer video id"""

    site: str | None = None
    """The site the video is hosted by (Currently either youtube or dailymotion)"""

    thumbnail: HttpUrl | None = None
    """The url for the thumbnail image of the video"""


class MediaCoverImage(ParentModel):
    """The cover images of the media."""

    extra_large: HttpUrl | None = None
    """The cover image url of the media at its largest size. If this size isn't available, large will be provided instead."""

    large: HttpUrl | None = None
    """The cover image url of the media at a large size"""

    medium: HttpUrl | None = None
    """The cover image url of the media at medium size"""

    color: Color | None = None
    """Average #hex color of cover image"""


class MediaTag(ParentModel):
    """A tag that describes a theme or element of the media."""

    id: int | None = None
    """The id of the tag"""

    name: str | None = None
    """The name of the tag"""

    description: str | None = None
    """A general description of the tag"""

    category: str | None = None
    """The categories of tags this tag belongs to"""

    rank: int | None = None
    """The relevance ranking of the tag out of the 100 for this media"""

    is_general_spoiler: bool | None = None
    """If the tag could be a spoiler for any media"""

    is_media_spoiler: bool | None = None
    """If the tag is a spoiler for this media"""

    is_adult: bool | None = None
    """If the tag is only for adult 18+ media"""

    user_id: int | None = None
    """The user who submitted the tag"""


class AiringSchedule(ParentModel):
    """Media Airing Schedule."""

    id: int | None = None
    """The id of the airing schedule item"""

    airing_at: int | None = None
    """The time the episode airs at"""

    time_until_airing: int | None = None
    """Seconds until episode starts airing"""

    episode: int | None = None
    """The airing episode number"""

    media_id: int | None = None
    """The associate media id of the airing episode"""


class MediaExternalLink(ParentModel):
    """An external link to another site related to the media or staff member."""

    id: int | None = None
    """The id of the external link"""

    url: HttpUrl | None = None
    """The url of the external link or base url of link source"""

    site: str | None = None
    """The links website site name"""

    site_id: int | None = None
    """The links website site id"""

    type: ExternalLinkType | None = None

    language: str | None = None
    """Language the site content is in. See Staff language field for values."""

    color: Color | None = None

    icon: HttpUrl | None = None
    """The icon image url of the site. Not available for all links. Transparent PNG 64x64"""

    notes: str | None = None

    is_disabled: bool | None = None


class MediaStreamingEpisode(ParentModel):
    """Data and links to legal streaming episodes on external sites."""

    title: str | None = None
    """Title of the episode"""

    thumbnail: HttpUrl | None = None
    """Url of episode image thumbnail"""

    url: HttpUrl | None = None
    """The url of the episode"""

    site: str | None = None
    """The site location of the streaming episodes"""


class Studio(ParentModel):
    """Animation or production company"""

    id: int | None = None
    """The id of the studio"""

    name: str | None = None
    """The name of the studio"""

    is_animation_studio: bool | None = None
    """If the studio is an animation studio or a different kind of company"""

    site_url: HttpUrl | None = None
    """The url for the studio page on the AniList website"""

    favourites: int | None = None
    """The amount of user's who have favourited the studio"""

    is_main: bool | None = None
    """If the studio is the main animation studio of the anime"""


class CharacterName(ParentModel):
    """The names of the character"""

    first: str | None = None
    """The character's given name"""

    middle: str | None = None
    """The character's middle name"""

    last: str | None = None
    """The character's surname"""

    full: str | None = None
    """The character's first and last name"""

    native: str | None = None
    """The character's full name in their native language"""

    alternative: tuple[str, ...] = tuple()
    """Other names the character might be referred to as"""

    alternative_spoiler: tuple[str, ...] = tuple()
    """Other names the character might be referred to as but are spoilers"""


class CharacterImage(ParentModel):
    """Character's image"""

    large: HttpUrl | None = None
    """The character's image of media at its largest size"""

    medium: HttpUrl | None = None
    """The character's image of media at medium size"""


class Character(ParentModel):
    """A character that features in an anime or manga"""

    id: int
    """The id of the character"""

    name: CharacterName = CharacterName()
    """The names of the character"""

    image: CharacterImage = CharacterImage()
    """Character images"""

    description: str | None = None
    """A general description of the character"""

    gender: str | None = None
    """The character's gender. Usually Male, Female, or Non-binary but can be any string."""

    date_of_birth: FuzzyDate = FuzzyDate()
    """The character's birth date"""

    age: str | None = None
    """The character's age. Note this is a string, not an int, it may contain further text and additional ages."""

    blood_type: str | None = None
    """The characters blood type"""

    site_url: HttpUrl | None = None
    """The url for the character page on the AniList website"""

    favourites: int | None = None
    """The amount of user's who have favourited the character"""

    role: CharacterRole | None = None
    """The characters role in the media"""


class StaffName(ParentModel):
    """The names of the staff member"""

    first: str | None = None
    """The person's given name"""

    middle: str | None = None
    """The person's middle name"""

    last: str | None = None
    """The person's surname"""

    full: str | None = None
    """The person's first and last name"""

    native: str | None = None
    """The person's full name in their native language"""

    alternative: tuple[str, ...] = tuple()
    """Other names the staff member might be referred to as (pen names)"""


class StaffImage(ParentModel):
    """Staff's image"""

    large: HttpUrl | None = None
    """The person's image of media at its largest size"""

    medium: HttpUrl | None = None
    """The person's image of media at medium size"""


class Staff(ParentModel):
    """Voice actors or production staff"""

    id: int | None = None
    """The id of the staff member"""

    name: StaffName = StaffName()
    """The names of the staff member"""

    language_v2: str | None = None
    """
    The primary language of the staff member. 
    Current values: Japanese, English, Korean, 
    Italian, Spanish, Portuguese, French, German, 
    Hebrew, Hungarian, Chinese, Arabic, Filipino, 
    Catalan, Finnish, Turkish, Dutch, Swedish, Thai, 
    Tagalog, Malaysian, Indonesian, Vietnamese, Nepali, 
    Hindi, Urdu
    """

    image: StaffImage = StaffImage()
    """The staff images"""

    description: str | None = None
    """A general description of the staff member"""

    primary_occupations: tuple[str, ...] = tuple()
    """The person's primary occupations"""

    gender: str | None = None
    """The staff's gender. Usually Male, Female, or Non-binary but can be any string."""

    date_of_birth: FuzzyDate = FuzzyDate()
    """The staff's date of birth."""

    date_of_death: FuzzyDate = FuzzyDate()
    """The staff's date of death."""

    age: int | None = None
    """The person's age in years"""

    years_active: YearsActive = YearsActive()
    """(start_year, end_year) (If the 2nd value is not present staff is still active)"""

    home_town: str | None = None
    """The persons birthplace or hometown"""

    blood_type: str | None = None
    """The persons blood type"""

    site_url: HttpUrl | None = None
    """The url for the staff page on the AniList website"""

    role: str | None = None
    """The role of the staff member in the production of the media"""


class MediaRank(ParentModel):
    """The ranking of a media in a particular time span and format compared to other media"""

    id: int | None = None
    """The id of the rank"""

    rank: int | None = None
    """The numerical rank of the media"""

    type: MediaRankType | None = None
    """The type of ranking"""

    format: MediaFormat | None = None
    """The format the media is ranked within"""

    year: int | None = None
    """The year the media is ranked within"""

    season: MediaSeason | None = None
    """The season the media is ranked within"""

    all_time: bool | None = None
    """If the ranking is based on all time instead of a season/year"""

    context: str | None = None
    """String that gives context to the ranking type and time span"""


class Relation(ParentModel):
    """Related Anime or Manga to parent Media"""

    id: int
    """The id of the media"""

    id_mal: int | None = None
    """The mal id of the media"""

    title: MediaTitle = MediaTitle()
    """The official titles of the media in various languages"""

    type: MediaType | None = None
    """The type of the media; anime or manga"""

    format: MediaFormat | None = None
    """The format the media was released in"""

    status: MediaStatus | None = None
    """The current releasing status of the media"""

    description: str | None = None
    """Short description of the media's story and characters"""

    start_date: FuzzyDate = FuzzyDate()
    """The first official release date of the media"""

    end_date: FuzzyDate = FuzzyDate()
    """The last official release date of the media"""

    season: MediaSeason | None = None
    """The season the media was initially released in"""

    season_year: int | None = None
    """The season year the media was initially released in"""

    season_int: int | None = None
    """The year & season the media was initially released in"""

    episodes: int | None = None
    """The amount of episodes the anime has when complete"""

    duration: int | None = None
    """The general length of each anime episode in minutes"""

    chapters: int | None = None
    """The amount of chapters the manga has when complete"""

    volumes: int | None = None
    """The amount of volumes the manga has when complete"""

    country_of_origin: CountryCode | None = None
    """Where the media was created. (ISO 3166-1 alpha-2)"""

    is_licensed: bool | None = None
    """If the media is officially licensed or a self-published doujin release"""

    source: MediaSource | None = None
    """Source type the media was adapted from."""

    hashtag: str | None = None
    """Official Twitter hashtags for the media"""

    trailer: MediaTrailer = MediaTrailer()
    """Media trailer or advertisement"""

    updated_at: datetime
    """When the media's data was last updated"""

    cover_image: MediaCoverImage = MediaCoverImage()
    """The cover images of the media"""

    banner_image: HttpUrl | None = None
    """The banner image of the media"""

    genres: tuple[str, ...] = tuple()
    """The genres of the media"""

    synonyms: tuple[str, ...] = tuple()
    """Alternative titles of the media"""

    average_score: int | None = None
    """A weighted average score of all the user's scores of the media"""

    mean_score: int | None = None
    """Mean score of all the user's scores of the media"""

    popularity: int | None = None
    """The number of users with the media on their list"""

    is_locked: bool | None = None
    """Locked media may not be added to lists our favorited. This may be due to the entry pending for deletion or other reasons."""

    trending: int | None = None
    """The amount of related activity in the past hour"""

    favourites: int | None = None
    """The amount of user's who have favourited the media"""

    tags: tuple[MediaTag, ...] = tuple()
    """List of tags that describes elements and themes of the media"""

    is_adult: bool | None = None
    """If the media is intended only for 18+ adult audiences"""

    next_airing_episode: AiringSchedule = AiringSchedule()
    """The media's next episode airing schedule"""

    external_links: tuple[MediaExternalLink, ...] = tuple()
    """External links to another site related to the media"""

    streaming_episodes: tuple[MediaStreamingEpisode, ...] = tuple()
    """Data and links to legal streaming episodes on external sites"""

    rankings: tuple[MediaRank, ...] = tuple()
    """The ranking of the media in a particular time span and format compared to other media"""

    site_url: HttpUrl | None = None
    """The url for the media page on the AniList website"""

    relation_type: MediaRelation | None = None
    "The type of relation to the parent model"


class Media(ParentModel):
    """Anime or Manga."""

    id: int
    """The id of the media"""

    id_mal: int | None = None
    """The mal id of the media"""

    title: MediaTitle = MediaTitle()
    """The official titles of the media in various languages"""

    type: MediaType | None = None
    """The type of the media; anime or manga"""

    format: MediaFormat | None = None
    """The format the media was released in"""

    status: MediaStatus | None = None
    """The current releasing status of the media"""

    description: str | None = None
    """Short description of the media's story and characters"""

    start_date: FuzzyDate = FuzzyDate()
    """The first official release date of the media"""

    end_date: FuzzyDate = FuzzyDate()
    """The last official release date of the media"""

    season: MediaSeason | None = None
    """The season the media was initially released in"""

    season_year: int | None = None
    """The season year the media was initially released in"""

    season_int: int | None = None
    """The year & season the media was initially released in"""

    episodes: int | None = None
    """The amount of episodes the anime has when complete"""

    duration: int | None = None
    """The general length of each anime episode in minutes"""

    chapters: int | None = None
    """The amount of chapters the manga has when complete"""

    volumes: int | None = None
    """The amount of volumes the manga has when complete"""

    country_of_origin: CountryCode | None = None
    """Where the media was created. (ISO 3166-1 alpha-2)"""

    is_licensed: bool | None = None
    """If the media is officially licensed or a self-published doujin release"""

    source: MediaSource | None = None
    """Source type the media was adapted from."""

    hashtag: str | None = None
    """Official Twitter hashtags for the media"""

    trailer: MediaTrailer = MediaTrailer()
    """Media trailer or advertisement"""

    updated_at: datetime
    """When the media's data was last updated"""

    cover_image: MediaCoverImage = MediaCoverImage()
    """The cover images of the media"""

    banner_image: HttpUrl | None = None
    """The banner image of the media"""

    genres: tuple[str, ...] = tuple()
    """The genres of the media"""

    synonyms: tuple[str, ...] = tuple()
    """Alternative titles of the media"""

    average_score: int | None = None
    """A weighted average score of all the user's scores of the media"""

    mean_score: int | None = None
    """Mean score of all the user's scores of the media"""

    popularity: int | None = None
    """The number of users with the media on their list"""

    is_locked: bool | None = None
    """Locked media may not be added to lists our favorited. This may be due to the entry pending for deletion or other reasons."""

    trending: int | None = None
    """The amount of related activity in the past hour"""

    favourites: int | None = None
    """The amount of user's who have favourited the media"""

    tags: tuple[MediaTag, ...] = tuple()
    """List of tags that describes elements and themes of the media"""

    relations: tuple[Relation, ...] = tuple()
    """Other media in the same or connecting franchise"""

    characters: tuple[Character, ...] = tuple()
    """The characters in the media"""

    staff: tuple[Staff, ...] = tuple()
    """Animation or production company"""

    studios: tuple[Studio, ...] = tuple()
    """Animation or production company"""

    is_adult: bool | None = None
    """If the media is intended only for 18+ adult audiences"""

    next_airing_episode: AiringSchedule = AiringSchedule()
    """The media's next episode airing schedule"""

    external_links: tuple[MediaExternalLink, ...] = tuple()
    """External links to another site related to the media"""

    streaming_episodes: tuple[MediaStreamingEpisode, ...] = tuple()
    """Data and links to legal streaming episodes on external sites"""

    rankings: tuple[MediaRank, ...] = tuple()
    """The ranking of the media in a particular time span and format compared to other media"""

    site_url: HttpUrl
    """The url for the media page on the AniList website"""


__all__ = [
    "AiringSchedule",
    "Character",
    "CharacterImage",
    "CharacterName",
    "FuzzyDate",
    "Media",
    "MediaCoverImage",
    "MediaExternalLink",
    "MediaRank",
    "MediaStreamingEpisode",
    "MediaTag",
    "MediaTitle",
    "MediaTrailer",
    "Relation",
    "Staff",
    "StaffImage",
    "StaffName",
    "Studio",
]
