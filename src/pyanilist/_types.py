from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator
from typing_extensions import NamedTuple

UTCDateTime = Annotated[datetime, AfterValidator(lambda dt: dt.astimezone(timezone.utc))]
"""datetime.datetime that's always in UTC."""


class YearsActive(NamedTuple):
    """
    Simple Named Tuple for
    [`Staff.years_active`][pyanilist._models.Staff.years_active].
    """

    start_year: int | None = None
    end_year: int | None = None
