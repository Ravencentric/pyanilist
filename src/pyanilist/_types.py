from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Annotated, TypeAlias, TypeVar

from pydantic import AfterValidator

if TYPE_CHECKING:
    from pyanilist._models import Media

T = TypeVar("T")

SortType: TypeAlias = Iterable[T] | T | None
"""
Represents the structure for AniList's sort parameter. 
It can be a single sort key, an iterable of sort keys, or None.
"""

MediaID: TypeAlias = "int | str | Media"
"""
Represents the different ways to identify media items. 
Can be an integer ID, a string URL, or a [`Media`][pyanilist.Media] object.
"""

UTCDateTime: TypeAlias = Annotated[datetime, AfterValidator(lambda dt: dt.astimezone(timezone.utc))]
"""Represents a [`datetime`][datetime.datetime] that's always in [`UTC`][datetime.timezone.utc]."""
