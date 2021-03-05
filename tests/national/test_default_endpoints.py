from lxml.etree import XMLSchema
import pytest

from carbon_intensity.models.measurements import MeasurementResponse
from carbon_intensity.models.factors import FactorResponse
from carbon_intensity.models.mixes import GenerationMixResponse
from carbon_intensity.api import JSONClient, XMLClient


@pytest.mark.usefixtures("json_api")
class TestNationalDefaultJSONEndpoints:
    def test_current_intensity(self, json_api: JSONClient) -> None:
        response = json_api.national.get_current_intensity()
        assert isinstance(response, MeasurementResponse)

    def test_today_intensity(self, json_api: JSONClient) -> None:
        response = json_api.national.get_today_intensity()
        assert isinstance(response, MeasurementResponse)

    def test_intensity_factors(self, json_api: JSONClient) -> None:
        response = json_api.national.get_intensity_factors()
        assert isinstance(response, FactorResponse)

    def test_current_generation_mix(self, json_api: JSONClient) -> None:
        response = json_api.national.get_current_generation_mix()
        assert isinstance(response, GenerationMixResponse)


@pytest.mark.usefixtures("xml_api", "measurement_schema", "factors_schema")
class TestNationalDefaultXMLEndpoints:
    def test_current_intensity(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_current_intensity()
        measurement_schema.assertValid(response.document)

    def test_today_intensity(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_today_intensity()
        measurement_schema.assertValid(response.document)

    def test_intensity_factors(
        self, xml_api: XMLClient, factors_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_factors()
        factors_schema.assertValid(response.document)
