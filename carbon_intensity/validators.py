from typing import Union, Optional
from datetime import datetime

from carbon_intensity.exceptions import APIConstraintException
from carbon_intensity.constants import MIN_PERIOD, MAX_PERIOD, ALLOWED_PENDULUM_ARGS


def check_period(period: Optional[int]) -> None:
    if period is not None and (period < MIN_PERIOD or period > MAX_PERIOD):
        raise APIConstraintException(
            f"Period must be an integer between {MIN_PERIOD} and {MAX_PERIOD}"
        )


def check_pendulum(**kwargs) -> None:
    pendulum_args = set(kwargs.keys())

    if not pendulum_args or not pendulum_args.issubset(ALLOWED_PENDULUM_ARGS):
        raise APIConstraintException(
            f"The allowed keywords for time interval are {ALLOWED_PENDULUM_ARGS}. "
            f"Use only or at least one of them."
        )


def check_interval(start_time: datetime, end_time: datetime) -> None:
    if start_time > end_time:
        raise APIConstraintException(
            f"API only allows start_time to be an early date than end_time"
        )
