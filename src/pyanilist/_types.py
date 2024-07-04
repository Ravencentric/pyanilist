"""
Aside from providing it's own types, this module also re-exports the following from pydantic for convenience:
- [HttpUrl](https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl)
- [Color](https://docs.pydantic.dev/latest/api/pydantic_extra_types_color/#pydantic_extra_types.color.Color)
- [CountryAlpha2 as CountryCoude](https://docs.pydantic.dev/latest/api/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2)
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field
from typing_extensions import NamedTuple


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    `_models.Staff.years_active`
    """

    start_year: int | None = None
    end_year: int | None = None


FuzzyDateInt = Annotated[
    int,
    Field(
        ge=10000000,
        le=99999999,
        description="8 digit long date integer (YYYYMMDD). Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500",
    ),
]


__all__ = [
    "YearsActive",
]
