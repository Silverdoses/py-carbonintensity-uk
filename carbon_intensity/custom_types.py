from datetime import date, datetime
from typing import Union

from pydantic import conint, constr
from pendulum import Date, DateTime

from .constants import MIN_PERIOD, MAX_PERIOD, ALLOWED_COUNTRIES_REGEX


AnyDateTime = Union[date, datetime, DateTime]
AnyDate = Union[date, Date]
PeriodInteger = conint(ge=MIN_PERIOD, le=MAX_PERIOD)
RegionString = constr(to_lower=True, regex=ALLOWED_COUNTRIES_REGEX)
