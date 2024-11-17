from __future__ import annotations

from httpx import HTTPStatusError

from ._client import AniList
from ._enums import (
    CharacterRole,
    CharacterSort,
    ExternalLinkType,
    MediaFormat,
    MediaRankType,
    MediaRelation,
    MediaSeason,
    MediaSort,
    MediaSource,
    MediaStatus,
    MediaType,
    RecommendationSort,
    StaffSort,
    StudioSort,
)
from ._models import (
    AiringSchedule,
    Character,
    CharacterImage,
    CharacterName,
    FuzzyDate,
    Media,
    MediaCoverImage,
    MediaExternalLink,
    MediaRank,
    MediaStreamingEpisode,
    MediaTag,
    MediaTitle,
    MediaTrailer,
    RelatedMedia,
    Staff,
    StaffImage,
    StaffName,
    Studio,
)
from ._types import YearsActive
from ._version import __version__, __version_tuple__

__all__ = [
    # Client
    "AniList",
    # Enums
    "CharacterRole",
    "CharacterSort",
    "ExternalLinkType",
    "MediaFormat",
    "MediaRankType",
    "MediaRelation",
    "MediaSeason",
    "MediaSort",
    "MediaSource",
    "MediaStatus",
    "MediaType",
    "RecommendationSort",
    "StaffSort",
    "StudioSort",
    # Types
    "YearsActive",
    # Models
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
    "RelatedMedia",
    "Staff",
    "StaffImage",
    "StaffName",
    "Studio",
    # Exceptions
    "HTTPStatusError",
    # Version
    "__version__",
    "__version_tuple__",
]
