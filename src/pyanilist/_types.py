"""
Aside from providing it's own types, this module also re-exports the following from pydantic for convenience:
- [HttpUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
- [Color](https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/#pydantic_extra_types.color.Color)
- [CountryAlpha2 as CountryCoude](https://docs.pydantic.dev/latest/api/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2)
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field, HttpUrl
from pydantic_extra_types.color import Color
from pydantic_extra_types.country import CountryAlpha2 as CountryCode
from typing_extensions import NamedTuple


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    `_models.Staff.years_active`
    """

    start_year: int | None = None
    end_year: int | None = None


AnilistID = Annotated[int, Field(gt=0, description="Anilist ID as found in the URL: https://anilist.co/{type}/{id}")]
AnilistYear = Annotated[int, Field(ge=1000, description="Release Year")]
AnilistTitle = Annotated[str, Field(min_length=1, description="Title of the media")]


__all__ = [
    "AnilistID",
    "AnilistTitle",
    "AnilistYear",
    "Color",
    "CountryCode",
    "HttpUrl",
    "YearsActive",
]