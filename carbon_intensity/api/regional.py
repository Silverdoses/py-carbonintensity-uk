from pydantic import validate_arguments
from requests import Session

from .base import BaseAPI
from ..models.regional import RegionListResponse, RegionResponse
from ..custom_types import RegionString
from ..constants import REGIONAL_INTENSITY_URL


class RegionalJSONAPI(BaseAPI):
    def __init__(self, session: Session, **kwargs):
        super().__init__(session=session, session_kwargs=kwargs)

    def get_current_intensity(self) -> RegionListResponse:
        response = self._request_as_json(method="get", url=REGIONAL_INTENSITY_URL)
        return RegionListResponse(**response)

    @validate_arguments
    def get_region_current_intensity(self, region: RegionString) -> RegionResponse:
        response = self._request_as_json(
            method="get", url=f"{REGIONAL_INTENSITY_URL}/{region}"
        )
        return RegionResponse(**response)
