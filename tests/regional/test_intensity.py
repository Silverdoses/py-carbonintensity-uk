from pydantic import ValidationError
import pytest

from carbon_intensity.models.regional import RegionListResponse, RegionResponse
from carbon_intensity.constants import ALLOWED_REGIONS
from carbon_intensity.api import JSONClient


@pytest.mark.usefixtures("json_api")
class TestRegionalIntensityByDateAsJSON:
    def test_current_intensity(self, json_api: JSONClient) -> None:
        response = json_api.regional.get_current_intensity()
        assert isinstance(response, RegionListResponse)

    @pytest.mark.parametrize("region", ALLOWED_REGIONS)
    def test_region_current_intensity(self, json_api: JSONClient, region: str) -> None:
        response = json_api.regional.get_region_current_intensity(region)
        assert isinstance(response, RegionResponse)

    def test_not_implemented_region(self, json_api: JSONClient) -> None:
        with pytest.raises(ValidationError):
            json_api.regional.get_region_current_intensity(region="fake_region")
