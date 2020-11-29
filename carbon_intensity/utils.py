from typing import Union, Tuple, Any, Optional
from datetime import datetime

from pendulum import DateTime

from carbon_intensity.exceptions import APITypeError


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


def normalize_date(date: Union[str, datetime, DateTime]) -> str:
    if issubclass(type(date), datetime):
        return date.strftime("%Y-%m-%d")
    elif type(date) == str:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            raise APITypeError(f"Date requires YYYY-MM-DD format - Got {date} instead")
    else:
        raise APITypeError(
            f"Required str or datetime as argument - Got {type(date).__name__} instead"
        )


def normalize_datetime(datetime_obj: datetime) -> str:
    if issubclass(type(datetime_obj), datetime):
        return datetime_obj.strftime("%Y-%m-%dT%H:%MZ")

    raise APITypeError(
        f"Required datetime as argument - Got {type(datetime_obj).__name__} instead"
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
