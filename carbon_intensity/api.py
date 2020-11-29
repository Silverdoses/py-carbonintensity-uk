from typing import Union, Dict, Optional
from datetime import datetime

import requests
import pendulum
from requests import Response
from dateutil.parser import parse as parse_date

from carbon_intensity import utils, validators
from carbon_intensity.exceptions import APIStatusError
from carbon_intensity.constants import (
    CURRENT_INTENSITY_URL,
    DAY_INTENSITY_URL,
    INTENSITY_FACTORS_URL,
)


class UKCarbonAPI:
    def __init__(self):
        self.session = requests.Session()

    def __del__(self):
        self.close()

    def __repr__(self) -> str:
        return f"Carbon Intensity API - {self.session.headers.get('User-Agent')}"

    def close(self) -> None:
        self.session.close()

    @staticmethod
    def _check_api_errors(response: Response) -> None:
        if response.status_code != 200:
            raise APIStatusError(f"API returned {response.status_code} status code")

    def _request_helper(self, url: str) -> Dict:
        response = self.session.get(url)
        self._check_api_errors(response)
        data = response.json()
        record = utils.recursive_parse(data, to_replace=("from", "to"), func=parse_date)
        return record

    # Default requests

    def get_current_intensity(self) -> Dict:
        return self._request_helper(url=CURRENT_INTENSITY_URL)

    def get_today_intensity(self) -> Dict:
        return self._request_helper(url=DAY_INTENSITY_URL)

    def get_intensity_factors(self) -> Dict:
        return self._request_helper(url=INTENSITY_FACTORS_URL)

    # Filter-capable requests

    def get_intensity_by_date(
        self, date: Union[datetime, str], period: Optional[int] = None
    ) -> Dict:

        period = utils.normalize_period(period)
        validators.check_period(period)
        parsed_date = utils.normalize_date(date)
        url = f"{DAY_INTENSITY_URL}/{parsed_date}"
        url += f"/{period}" if period else str()
        return self._request_helper(url)

    def get_intensity_at_time(self, time: datetime) -> Dict:
        parsed_time = utils.normalize_datetime(time)
        return self._request_helper(url=f"{CURRENT_INTENSITY_URL}/{parsed_time}")

    def get_forward_intensity(self, from_time: datetime, **kwargs) -> Dict:
        validators.check_pendulum(**kwargs)
        start_time = utils.normalize_datetime(from_time)
        end_time = utils.normalize_datetime(pendulum.instance(from_time).add(**kwargs))
        return self._request_helper(
            url=f"{CURRENT_INTENSITY_URL}/{start_time}/{end_time}"
        )

    def get_backward_intensity(self, from_time: datetime, **kwargs) -> Dict:
        validators.check_pendulum(**kwargs)
        start_time = utils.normalize_datetime(
            pendulum.instance(from_time).subtract(**kwargs)
        )
        end_time = utils.normalize_datetime(from_time)
        return self._request_helper(
            url=f"{CURRENT_INTENSITY_URL}/{start_time}/{end_time}"
        )

    def get_intensity_between(self, from_time: datetime, to_time: datetime) -> Dict:
        validators.check_interval(from_time, to_time)
        start_time = utils.normalize_datetime(from_time)
        end_time = utils.normalize_datetime(to_time)
        return self._request_helper(
            url=f"{CURRENT_INTENSITY_URL}/{start_time}/{end_time}"
        )
