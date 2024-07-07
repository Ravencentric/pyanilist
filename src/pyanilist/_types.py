from __future__ import annotations

from typing import Annotated

from pydantic import Field
from typing_extensions import NamedTuple, TypeAlias, TypeVar, Union

# A simpler Iterable type instead of collections.abc.Iterable
# to stop pydantic from converting them to ValidatorIterator
# https://github.com/pydantic/pydantic/issues/9541
T = TypeVar("T")
CollectionOf: TypeAlias = Union[set[T], tuple[T, ...], list[T]]


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    [`Staff.years_active`][pyanilist._models.Staff.years_active]
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
"""8 digit long date integer (YYYYMMDD). Unknown dates represented by 0. E.g. 2016: 20160000, May 1976: 19760500"""
