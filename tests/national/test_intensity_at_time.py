from lxml.etree import XMLSchema
import pytest

from carbon_intensity.models.measurements import MeasurementResponse
from carbon_intensity.api import JSONClient, XMLClient
from ..conftest import today


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityAtTimeAsJSON:
    def test_intensity_at_time(self, json_api: JSONClient):
        response = json_api.national.get_intensity_at(time=today)
        assert isinstance(response, MeasurementResponse)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityAtTimeAsXML:
    def test_intensity_at_time(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_at(time=today)
        measurement_schema.assertValid(response.document)
