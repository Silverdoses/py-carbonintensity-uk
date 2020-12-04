from typing import Union, Tuple, Any, Optional
from datetime import datetime

from pendulum import DateTime
from dateutil.parser import parse as parse_date

from carbon_intensity.exceptions import APITypeError
from carbon_intensity.constants import API_DATE_FORMAT, API_DATETIME_FORMAT


def recursive_parse(data: Any, to_replace: Tuple, func: Any) -> Any:

    if type(data) == dict:
        return {
            key: recursive_parse(func(value), to_replace, func)
            if key in to_replace
            else recursive_parse(value, to_replace, func)
            for key, value in data.items()
        }
    elif type(data) in (list, set):
        return [recursive_parse(item, to_replace, func) for item in data]
    else:
        return data


def normalize_datetime(
    date: Union[str, datetime, DateTime], only_date: bool = False
) -> str:

    if issubclass(type(date), datetime):
        return date.strftime(API_DATE_FORMAT if only_date else API_DATETIME_FORMAT)
    elif type(date) == str:
        try:
            date_obj = parse_date(date)
            return date_obj.strftime(API_DATE_FORMAT)
        except ValueError:
            raise APITypeError(f"Date requires YYYY-MM-DD format - Got {date} instead")
    else:
        raise APITypeError(
            f"Required str or datetime as argument - Got {type(date).__name__} instead"
        )


def normalize_period(period: Optional[Union[int, float, str]]) -> Optional[int]:
    try:
        return int(period) if period is not None else None
    except (
        ValueError,
        TypeError,
    ):
        raise APITypeError(
            f"Required int, float or str as argument - Got {type(period).__name__} instead"
        )
