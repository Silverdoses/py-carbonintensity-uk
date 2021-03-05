from typing import Optional, Any

from pydantic import validate_arguments
from requests import Session

from .base import BaseAPI
from ..models.base import XMLResponse
from ..models.measurements import MeasurementResponse
from ..models.factors import FactorResponse
from ..models.mixes import GenerationMixResponse
from ..custom_types import AnyDate, PeriodInteger, AnyDateTime
from ..constants import (
    CURRENT_INTENSITY_URL,
    INTENSITY_BY_DATE_URL,
    INTENSITY_FACTORS_URL,
    GENERATION_MIX_URL,
    CURRENT_INTENSITY_URL_XML,
    INTENSITY_BY_DATE_URL_XML,
    INTENSITY_FACTORS_URL_XML,
)


class NationalJSONAPI(BaseAPI):
    def __init__(self, session: Session, **kwargs: Any):
        super().__init__(session=session, session_kwargs=kwargs)

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
    def get_current_generation_mix(self) -> GenerationMixResponse:
        response = self._request_as_json(method="get", url=GENERATION_MIX_URL)
        return GenerationMixResponse(**response)

    @validate_arguments
    def get_intensity_by_date(
        self, date: AnyDate, period: Optional[PeriodInteger] = None
    ) -> MeasurementResponse:
        endpoint = f"{INTENSITY_BY_DATE_URL}/{date}"
        endpoint += f"/{period}" if period else str()
        response = self._request_as_json(method="get", url=endpoint)
        return MeasurementResponse(**response)

    @validate_arguments
    def get_intensity_at(self, time: AnyDateTime) -> MeasurementResponse:
        response = self._request_as_json(
            method="get", url=f"{CURRENT_INTENSITY_URL}/{time}"
        )
        return MeasurementResponse(**response)


class NationalXMLAPI(BaseAPI):
    def __init__(self, session: Session, **kwargs):
        super().__init__(session=session, session_kwargs=kwargs)

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
        endpoint = f"{INTENSITY_BY_DATE_URL_XML}/{date}"
        endpoint += f"/{period}" if period else str()
        response = self._request_as_xml(method="get", url=endpoint)
        return XMLResponse(response)

    @validate_arguments
    def get_intensity_at(self, time: AnyDateTime) -> XMLResponse:
        response = self._request_as_xml(
            method="get", url=f"{CURRENT_INTENSITY_URL_XML}/{time}"
        )
        return XMLResponse(response)
