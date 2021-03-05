import random

from pydantic import ValidationError
from lxml.etree import XMLSchema
import pendulum
import pytest

from carbon_intensity.models.measurements import MeasurementResponse
from carbon_intensity.constants import MIN_PERIOD, MAX_PERIOD
from carbon_intensity.api import JSONClient, XMLClient


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityByDateAsJSON:
    def test_without_period(self, json_api: JSONClient) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        response = json_api.national.get_intensity_by_date(date=yesterday)
        assert isinstance(response, MeasurementResponse)

    def test_with_valid_period(self, json_api: JSONClient) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        period = random.randrange(MIN_PERIOD, MAX_PERIOD)
        response = json_api.national.get_intensity_by_date(
            date=yesterday, period=period
        )
        assert isinstance(response, MeasurementResponse)

    def test_with_invalid_greater_period(self, json_api: JSONClient) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        period = MAX_PERIOD + 1

        with pytest.raises(ValidationError):
            json_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_lesser_period(self, json_api: JSONClient) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
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
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        response = xml_api.national.get_intensity_by_date(date=yesterday)
        measurement_schema.assertValid(response.document)

    def test_with_valid_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        period = random.randrange(MIN_PERIOD, MAX_PERIOD)
        response = xml_api.national.get_intensity_by_date(date=yesterday, period=period)
        measurement_schema.assertValid(response.document)

    def test_with_invalid_greater_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        period = MAX_PERIOD + 1

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_lesser_period(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        yesterday = pendulum.now(tz="UTC").subtract(days=1)
        period = MIN_PERIOD - 1

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=yesterday, period=period)

    def test_with_invalid_date(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        invalid_date = "1234-56-78"

        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_by_date(date=invalid_date)


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityAtTimeAsJSON:
    def test_intensity_at_time(self, json_api: JSONClient):
        today = pendulum.today(tz="UTC")
        response = json_api.national.get_intensity_at(time=today)
        assert isinstance(response, MeasurementResponse)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityAtTimeAsXML:
    def test_intensity_at_time(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        today = pendulum.today(tz="UTC")
        response = xml_api.national.get_intensity_at(time=today)
        measurement_schema.assertValid(response.document)
