from __future__ import annotations

from ._compat import StrEnum


class BaseStrEnum(StrEnum):
    @property
    def title(self) -> str:  # type: ignore
        """
        Title Cased value
        """

        # These don't get the desired results with .title()
        # so we manually map them
        exceptions = {
            "TV": "TV",
            "TV_SHORT": "TV Short",
            "OVA": "OVA",
            "ONA": "ONA",
            "ID": "ID",
            "ID_DESC": "ID Desc",
        }

        if self.value in exceptions:
            return exceptions[self.value]

        return self.value.replace("_", " ").title()


class MediaType(BaseStrEnum):
    """The type of the media; anime or manga."""

    ANIME = "ANIME"
    """Japanese Anime"""

    MANGA = "MANGA"
    """Asian comic"""


class MediaFormat(BaseStrEnum):
    """The format the media was released in."""

    TV = "TV"
    """Anime broadcast on television"""

    TV_SHORT = "TV_SHORT"
    """Anime which are under 15 minutes in length and broadcast on television"""

    MOVIE = "MOVIE"
    """Anime movies with a theatrical release"""

    SPECIAL = "SPECIAL"
    """Special episodes that have been included in DVD/Blu-ray releases, picture dramas, pilots, etc"""

    OVA = "OVA"
    """
    (Original Video Animation)
    Anime that have been released directly on DVD/Blu-ray without 
    originally going through a theatrical release or television broadcast
    """

    ONA = "ONA"
    """
    (Original Net Animation) 
    Anime that have been originally released online or are only available through streaming services
    """

    MUSIC = "MUSIC"
    """Short anime released as a music video"""

    MANGA = "MANGA"
    """Professionally published manga with more than one chapter"""

    NOVEL = "NOVEL"
    """Written books released as a series of light novels"""

    ONE_SHOT = "ONE_SHOT"
    """Manga with just one chapter"""


class MediaStatus(BaseStrEnum):
    """The current releasing status of the media."""

    FINISHED = "FINISHED"
    """Has completed and is no longer being released"""

    RELEASING = "RELEASING"
    """Currently releasing"""

    NOT_YET_RELEASED = "NOT_YET_RELEASED"
    """To be released at a later date"""

    CANCELLED = "CANCELLED"
    """Ended before the work could be finished"""

    HIATUS = "HIATUS"
    """Version 2 only. Is currently paused from releasing and will resume at a later date"""


class MediaSeason(BaseStrEnum):
    """The season the media was initially released in."""

    WINTER = "WINTER"
    """Months December to February"""

    SPRING = "SPRING"
    """Months March to May"""

    SUMMER = "SUMMER"
    """Months June to August"""

    FALL = "FALL"
    """Months September to November"""


class MediaSource(BaseStrEnum):
    """Source type the media was adapted from."""

    ORIGINAL = "ORIGINAL"
    """An original production not based of another work"""

    MANGA = "MANGA"
    """Asian comic book"""

    LIGHT_NOVEL = "LIGHT_NOVEL"
    """Written work published in volumes"""

    VISUAL_NOVEL = "VISUAL_NOVEL"
    """Video game driven primary by text and narrative"""

    VIDEO_GAME = "VIDEO_GAME"
    """Video game"""

    OTHER = "OTHER"
    """Other"""

    NOVEL = "NOVEL"
    """Version 2+ only. Written works not published in volumes"""

    DOUJINSHI = "DOUJINSHI"
    """Version 2+ only. Self-published works"""

    ANIME = "ANIME"
    """Version 2+ only. Japanese Anime"""

    WEB_NOVEL = "WEB_NOVEL"
    """Version 3 only. Written works published online"""

    LIVE_ACTION = "LIVE_ACTION"
    """Version 3 only. Live action media such as movies or TV show"""

    GAME = "GAME"
    """Version 3 only. Games excluding video games"""

    COMIC = "COMIC"
    """Version 3 only. Comics excluding manga"""

    MULTIMEDIA_PROJECT = "MULTIMEDIA_PROJECT"
    """Version 3 only. Multimedia project"""

    PICTURE_BOOK = "PICTURE_BOOK"
    """Version 3 only. Picture book"""


class MediaRelation(BaseStrEnum):
    """Type of relation media has to its parent."""

    ADAPTATION = "ADAPTATION"
    """An adaptation of this media into a different format"""

    PREQUEL = "PREQUEL"
    """Released before the relation"""

    SEQUEL = "SEQUEL"
    """Released after the relation"""

    PARENT = "PARENT"
    """The media a side story is from"""

    SIDE_STORY = "SIDE_STORY"
    """A side story of the parent media"""

    CHARACTER = "CHARACTER"
    """Shares at least 1 character"""

    SUMMARY = "SUMMARY"
    """A shortened and summarized version"""

    ALTERNATIVE = "ALTERNATIVE"
    """An alternative version of the same media"""

    SPIN_OFF = "SPIN_OFF"
    """An alternative version of the media with a different primary focus"""

    OTHER = "OTHER"
    """Other"""

    SOURCE = "SOURCE"
    """Version 2 only. The source material the media was adapted from"""

    COMPILATION = "COMPILATION"
    """Version 2 only."""

    CONTAINS = "CONTAINS"
    """Version 2 only."""


class ExternalLinkType(BaseStrEnum):
    """External Link Type"""

    INFO = "INFO"
    """Informational site"""

    SOCIAL = "SOCIAL"
    """Social media site"""

    STREAMING = "STREAMING"
    """Streaming site"""


class CharacterRole(BaseStrEnum):
    """The role the character plays in the media"""

    MAIN = "MAIN"
    """A primary character role in the media"""

    SUPPORTING = "SUPPORTING"
    """A supporting character role in the media"""

    BACKGROUND = "BACKGROUND"
    """A background character in the media"""


class MediaRankType(BaseStrEnum):
    """The type of ranking"""

    RATED = "RATED"
    """Ranking is based on the media's ratings/score"""

    POPULAR = "POPULAR"
    """Ranking is based on the media's popularity"""


class MediaSort(BaseStrEnum):
    """Media sort enums"""

    ID = "ID"
    ID_DESC = "ID_DESC"
    TITLE_ROMAJI = "TITLE_ROMAJI"
    TITLE_ROMAJI_DESC = "TITLE_ROMAJI_DESC"
    TITLE_ENGLISH = "TITLE_ENGLISH"
    TITLE_ENGLISH_DESC = "TITLE_ENGLISH_DESC"
    TITLE_NATIVE = "TITLE_NATIVE"
    TITLE_NATIVE_DESC = "TITLE_NATIVE_DESC"
    TYPE = "TYPE"
    TYPE_DESC = "TYPE_DESC"
    FORMAT = "FORMAT"
    FORMAT_DESC = "FORMAT_DESC"
    START_DATE = "START_DATE"
    START_DATE_DESC = "START_DATE_DESC"
    END_DATE = "END_DATE"
    END_DATE_DESC = "END_DATE_DESC"
    SCORE = "SCORE"
    SCORE_DESC = "SCORE_DESC"
    POPULARITY = "POPULARITY"
    POPULARITY_DESC = "POPULARITY_DESC"
    TRENDING = "TRENDING"
    TRENDING_DESC = "TRENDING_DESC"
    EPISODES = "EPISODES"
    EPISODES_DESC = "EPISODES_DESC"
    DURATION = "DURATION"
    DURATION_DESC = "DURATION_DESC"
    STATUS = "STATUS"
    STATUS_DESC = "STATUS_DESC"
    CHAPTERS = "CHAPTERS"
    CHAPTERS_DESC = "CHAPTERS_DESC"
    VOLUMES = "VOLUMES"
    VOLUMES_DESC = "VOLUMES_DESC"
    UPDATED_AT = "UPDATED_AT"
    UPDATED_AT_DESC = "UPDATED_AT_DESC"
    SEARCH_MATCH = "SEARCH_MATCH"
    FAVOURITES = "FAVOURITES"
    FAVOURITES_DESC = "FAVOURITES_DESC"


__all__ = [
    "CharacterRole",
    "ExternalLinkType",
    "MediaFormat",
    "MediaRankType",
    "MediaRelation",
    "MediaSeason",
    "MediaSort",
    "MediaSource",
    "MediaStatus",
    "MediaType",
]
