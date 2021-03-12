from typing import Any, Callable, Optional

from decorator import decorator
from pydantic import PositiveInt

from carbon_intensity.exceptions import APIConstraintException
from carbon_intensity.custom_types import AnyDate, AnyDateTime
from carbon_intensity.constants import (
    ALLOWED_PENDULUM_ARGS,
    API_DATETIME_FORMAT,
    API_DATE_FORMAT
)


@decorator
def only_pendulum_kwargs(func: Callable, *args: Any, **kwargs: Any) -> Callable:
    pendulum_args = set(kwargs.keys())

    if not pendulum_args or not pendulum_args.issubset(ALLOWED_PENDULUM_ARGS):
        raise APIConstraintException(
            f"The allowed keywords for time interval are {ALLOWED_PENDULUM_ARGS}. "
            f"Use only or at least one of them."
        )

    return func(*args, **kwargs)


@decorator
def check_interval(func: Callable, *args: Any, **kwargs: Any) -> Callable:
    _, start_time, end_time = args

    if start_time >= end_time:
        raise APIConstraintException(
            f"The start datetime should be less than the end datetime"
        )

    return func(*args, **kwargs)


@decorator
def max_interval(
    func: Callable, days: Optional[PositiveInt] = None, *args: Any, **kwargs: Any
) -> Callable:

    _, start_time, end_time, block = args

    if start_time >= end_time or (start_time - end_time).days > days:
        raise APIConstraintException(f"Interval between dates must be max {days} days")

    return func(*args, **kwargs)


def normalize_datetime(datetime_obj: AnyDateTime) -> str:
    return datetime_obj.strftime(API_DATETIME_FORMAT)


def normalize_date(date_obj: AnyDate) -> str:
    return date_obj.strftime(API_DATE_FORMAT)
