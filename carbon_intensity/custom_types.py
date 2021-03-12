from datetime import date, datetime
from typing import Union

from pydantic import conint, constr
from pendulum import Date, DateTime

from .constants import (
    MIN_PERIOD,
    MAX_PERIOD,
    ALLOWED_REGIONS_REGEX,
    MIN_HOURS_BLOCK,
    MAX_HOURS_BLOCK,
)


AnyDateTime = Union[date, datetime, DateTime]
AnyDate = Union[date, Date]
PeriodInteger = conint(ge=MIN_PERIOD, le=MAX_PERIOD)
BlockInteger = conint(ge=MIN_HOURS_BLOCK, le=MAX_HOURS_BLOCK)
RegionString = constr(to_lower=True, regex=ALLOWED_REGIONS_REGEX)
