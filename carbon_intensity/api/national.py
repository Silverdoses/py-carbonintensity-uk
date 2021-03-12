from typing import Optional, Any

from pydantic import validate_arguments, PositiveInt
from requests import Session

from .base import BaseAPI
from ..custom_types import AnyDate, PeriodInteger, AnyDateTime, BlockInteger
from ..models.stats import StatsListResponse
from ..models.measurements import MeasurementResponse
from ..models.factors import FactorResponse
from ..models.base import XMLResponse
from ..models.mixes import GenerationMixResponse, GenerationMixListResponse
from ..constraints import (
    check_interval,
    only_pendulum_kwargs,
    normalize_date,
    normalize_datetime,
    max_interval,
)
from ..constants import (
    CURRENT_INTENSITY_URL,
    INTENSITY_BY_DATE_URL,
    INTENSITY_FACTORS_URL,
    GENERATION_MIX_URL,
    CURRENT_INTENSITY_URL_XML,
    INTENSITY_BY_DATE_URL_XML,
    INTENSITY_FACTORS_URL_XML,
    INTENSITY_STATS_URL,
    INTENSITY_STATS_URL_XML,
)


class NationalJSONAPI(BaseAPI):
    def __init__(self, session: Session, **kwargs: Any):
        super().__init__(session=session, session_kwargs=kwargs)

    # Carbon Intensity - National

    def get_current_intensity(self) -> MeasurementResponse:
        response = self._request_as_json(method="get", url=CURRENT_INTENSITY_URL)
        return MeasurementResponse(**response)

    def get_today_intensity(self) -> MeasurementResponse:
        response = self._request_as_json(method="get", url=INTENSITY_BY_DATE_URL)
        return MeasurementResponse(**response)

    def get_intensity_factors(self) -> FactorResponse:
        response = self._request_as_json(method="get", url=INTENSITY_FACTORS_URL)
        return FactorResponse(**response)

    @validate_arguments
    def get_intensity_by_date(
        self, date: AnyDate, period: Optional[PeriodInteger] = None
    ) -> MeasurementResponse:
        endpoint = f"{INTENSITY_BY_DATE_URL}/{normalize_date(date)}"
        endpoint += f"/{period}" if period else str()
        response = self._request_as_json(method="get", url=endpoint)
        return MeasurementResponse(**response)

    @validate_arguments
    def get_intensity_at(self, time: AnyDateTime) -> MeasurementResponse:
        response = self._request_as_json(
            method="get", url=f"{CURRENT_INTENSITY_URL}/{normalize_datetime(time)}"
        )
        return MeasurementResponse(**response)

    @validate_arguments
    @only_pendulum_kwargs
    def get_intensity_after(
        self, from_: AnyDateTime, **kwargs: PositiveInt
    ) -> MeasurementResponse:
        start = normalize_datetime(from_)
        end = normalize_datetime(from_.add(**kwargs))
        response = self._request_as_json(
            method="get", url=f"{CURRENT_INTENSITY_URL}/{start}/{end}"
        )
        return MeasurementResponse(**response)

    @validate_arguments
    @only_pendulum_kwargs
    def get_intensity_before(
        self, from_: AnyDateTime, **kwargs: PositiveInt
    ) -> MeasurementResponse:
        start = normalize_datetime(from_.subtract(**kwargs))
        end = normalize_datetime(from_)
        response = self._request_as_json(
            method="get", url=f"{CURRENT_INTENSITY_URL}/{start}/{end}"
        )
        return MeasurementResponse(**response)

    @validate_arguments
    @check_interval
    def get_intensity_between(
        self, from_: AnyDateTime, to: AnyDateTime
    ) -> MeasurementResponse:
        start = normalize_datetime(from_)
        end = normalize_datetime(to)
        response = self._request_as_json(
            method="get", url=f"{CURRENT_INTENSITY_URL}/{start}/{end}"
        )
        return MeasurementResponse(**response)

    # Generation Mix - National (Beta)

    @validate_arguments
    def get_current_generation_mix(self) -> GenerationMixResponse:
        response = self._request_as_json(method="get", url=GENERATION_MIX_URL)
        return GenerationMixResponse(**response)

    @validate_arguments
    @only_pendulum_kwargs
    def get_generation_mix_before(
        self, from_: AnyDateTime, **kwargs: PositiveInt
    ) -> GenerationMixListResponse:
        start = normalize_datetime(from_.subtract(**kwargs))
        end = normalize_datetime(from_)
        response = self._request_as_json(
            method="get", url=f"{GENERATION_MIX_URL}/{start}/{end}"
        )
        return GenerationMixListResponse(**response)

    @validate_arguments
    @check_interval
    def get_generation_mix_between(
        self, from_: AnyDateTime, to: AnyDateTime
    ) -> GenerationMixListResponse:
        response = self._request_as_json(
            method="get", url=f"{GENERATION_MIX_URL}/{from_}/{to}"
        )
        return GenerationMixListResponse(**response)

    # Statistics - National

    @validate_arguments
    @max_interval(days=30)
    def get_intensity_stats_between(
        self, from_: AnyDateTime, to: AnyDateTime, block: Optional[BlockInteger] = None
    ) -> StatsListResponse:

        endpoint = f"{INTENSITY_STATS_URL}/{normalize_date(from_)}/{normalize_date(to)}"
        endpoint += f"/{block}" if block else str()
        response = self._request_as_json(method="get", url=endpoint)
        return StatsListResponse(**response)


class NationalXMLAPI(BaseAPI):
    def __init__(self, session: Session, **kwargs):
        super().__init__(session=session, session_kwargs=kwargs)

    # Carbon Intensity - National

    def get_current_intensity(self) -> XMLResponse:
        response = self._request_as_xml(method="get", url=CURRENT_INTENSITY_URL_XML)
        return XMLResponse(response)

    def get_today_intensity(self) -> XMLResponse:
        response = self._request_as_xml(method="get", url=INTENSITY_BY_DATE_URL_XML)
        return XMLResponse(response)

    def get_intensity_factors(self) -> XMLResponse:
        response = self._request_as_xml(method="get", url=INTENSITY_FACTORS_URL_XML)
        return XMLResponse(response)

    @validate_arguments
    def get_intensity_by_date(
        self, date: AnyDate, period: Optional[PeriodInteger] = None
    ) -> XMLResponse:
        endpoint = f"{INTENSITY_BY_DATE_URL_XML}/{normalize_date(date)}"
        endpoint += f"/{period}" if period else str()
        response = self._request_as_xml(method="get", url=endpoint)
        return XMLResponse(response)

    @validate_arguments
    def get_intensity_at(self, time: AnyDateTime) -> XMLResponse:
        response = self._request_as_xml(
            method="get",
            url=f"{CURRENT_INTENSITY_URL_XML}/{normalize_datetime(time)}"
        )
        return XMLResponse(response)

    @validate_arguments
    @only_pendulum_kwargs
    def get_intensity_after(
        self, from_: AnyDateTime, **kwargs: PositiveInt
    ) -> XMLResponse:
        start = normalize_datetime(from_)
        end = normalize_datetime(from_.add(**kwargs))
        response = self._request_as_xml(
            method="get", url=f"{CURRENT_INTENSITY_URL_XML}/{start}/{end}"
        )
        return XMLResponse(response)

    @validate_arguments
    @only_pendulum_kwargs
    def get_intensity_before(
        self, from_: AnyDateTime, **kwargs: PositiveInt
    ) -> XMLResponse:
        start = normalize_datetime(from_.subtract(**kwargs))
        end = normalize_datetime(from_)
        response = self._request_as_xml(
            method="get", url=f"{CURRENT_INTENSITY_URL_XML}/{start}/{end}"
        )
        return XMLResponse(response)

    @validate_arguments
    @check_interval
    def get_intensity_between(self, from_: AnyDateTime, to: AnyDateTime) -> XMLResponse:
        start = normalize_datetime(from_)
        end = normalize_datetime(to)
        response = self._request_as_xml(
            method="get", url=f"{CURRENT_INTENSITY_URL_XML}/{start}/{end}"
        )
        return XMLResponse(response)

    # Statistics - National

    @validate_arguments
    @max_interval(days=30)
    def get_intensity_stats_between(
        self, from_: AnyDateTime, to: AnyDateTime, block: Optional[BlockInteger] = None
    ) -> XMLResponse:

        endpoint = (
            f"{INTENSITY_STATS_URL_XML}/{normalize_date(from_)}/{normalize_date(to)}"
        )
        endpoint += f"/{block}" if block else str()
        response = self._request_as_xml(method="get", url=endpoint)
        return XMLResponse(response)
