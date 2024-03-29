"""
Aside from providing it's own types, this module also re-exports the following from pydantic for convenience:
- [HttpUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
- [Color](https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/#pydantic_extra_types.color.Color)
- [CountryAlpha2 as CountryCoude](https://docs.pydantic.dev/latest/api/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2)
"""

from __future__ import annotations

from typing import Annotated, Any

from pydantic import Field, HttpUrl
from pydantic_extra_types.color import Color
from pydantic_extra_types.country import CountryAlpha2 as CountryCode
from typing_extensions import NamedTuple, TypeAlias


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    `_models.Staff.years_active`
    """

    start_year: int | None = None
    end_year: int | None = None


AniListID = Annotated[int, Field(gt=0, description="AniList ID as found in the URL: https://anilist.co/{type}/{id}")]
AniListYear = Annotated[int, Field(ge=1000, description="Release Year")]
AniListTitle = Annotated[str, Field(min_length=1, description="Title of the media")]

HTTPXClientKwargs: TypeAlias = Any
"""Simple TypeAlias to refer to `httpx.Client()` kwargs"""

HTTPXAsyncClientKwargs: TypeAlias = Any
"""Simple TypeAlias to refer to `httpx.AsyncClient()` kwargs"""

__all__ = [
    "AniListID",
    "AniListTitle",
    "AniListYear",
    "Color",
    "CountryCode",
    "HttpUrl",
    "YearsActive",
]
