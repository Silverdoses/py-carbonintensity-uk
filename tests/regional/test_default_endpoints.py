import pytest

from carbon_intensity.models.regional import RegionListResponse
from carbon_intensity.api import JSONClient


@pytest.mark.usefixtures("json_api")
class TestRegionalDefaultJSONEndpoints:
    def test_current_regional_intensity(self, json_api: JSONClient) -> None:
        response = json_api.regional.get_current_intensity()
        assert isinstance(response, RegionListResponse)
