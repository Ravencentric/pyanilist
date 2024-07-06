from __future__ import annotations

from httpx import HTTPStatusError
from pydantic import ValidationError

from ._clients import AniList, AsyncAniList
from ._enums import (
    CharacterRole,
    ExternalLinkType,
    MediaFormat,
    MediaRankType,
    MediaRelation,
    MediaSeason,
    MediaSort,
    MediaSource,
    MediaStatus,
    MediaType,
)
from ._models import (
    AiringSchedule,
    Character,
    CharacterImage,
    CharacterName,
    FuzzyDate,
    Media,
    MediaCoverImage,
    MediaDescription,
    MediaExternalLink,
    MediaRank,
    MediaStreamingEpisode,
    MediaTag,
    MediaTitle,
    MediaTrailer,
    Relation,
    Staff,
    StaffImage,
    StaffName,
    Studio,
)
from ._types import FuzzyDateInt, YearsActive
from ._version import Version, _get_version

__version__ = _get_version()
__version_tuple__ = Version(*map(int, __version__.split(".")))

__all__ = [
    # Clients
    "AsyncAniList",
    "AniList",
    # Enums
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
    # Types
    "YearsActive",
    "FuzzyDateInt",
    # Models
    "AiringSchedule",
    "Character",
    "CharacterImage",
    "CharacterName",
    "FuzzyDate",
    "Media",
    "MediaCoverImage",
    "MediaDescription",
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
    # Exceptions
    "HTTPStatusError",
    "ValidationError",
]
