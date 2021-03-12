import random

from pydantic import ValidationError
from lxml.etree import XMLSchema
import pytest

from carbon_intensity.models.measurements import MeasurementResponse
from carbon_intensity.constants import MIN_PERIOD, MAX_PERIOD
from carbon_intensity.api import JSONClient, XMLClient
from ..conftest import yesterday


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityByDateAsJSON:
    def test_without_period(self, json_api: JSONClient) -> None:
        response = json_api.national.get_intensity_by_date(date=yesterday)
        assert isinstance(response, MeasurementResponse)

    def test_with_valid_period(self, json_api: JSONClient) -> None:
        period = random.randrange(MIN_PERIOD, MAX_PERIOD)
        response = json_api.national.get_intensity_by_date(
            date=yesterday,
            period=period
        )
        assert isinstance(response, MeasurementResponse)

    def test_with_invalid_greater_period(self, json_api: JSONClient) -> None:
        period = MAX_PERIOD + 1

        with pytest.raises(ValidationError):
            json_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_lesser_period(self, json_api: JSONClient) -> None:
        period = MIN_PERIOD - 1

        with pytest.raises(ValidationError):
            json_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_date(self, json_api: JSONClient) -> None:
        invalid_date = "1234-56-78"

        with pytest.raises(ValidationError):
            json_api.national.get_intensity_by_date(date=invalid_date)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityByDateAsXML:
    def test_without_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_by_date(date=yesterday)
        measurement_schema.assertValid(response.document)

    def test_with_valid_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        period = random.randrange(MIN_PERIOD, MAX_PERIOD)
        response = xml_api.national.get_intensity_by_date(date=yesterday, period=period)
        measurement_schema.assertValid(response.document)

    def test_with_invalid_greater_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        period = MAX_PERIOD + 1

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_lesser_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        period = MIN_PERIOD - 1

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_date(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        invalid_date = "1234-56-78"

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=invalid_date)
