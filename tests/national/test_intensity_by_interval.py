from pydantic import ValidationError
from lxml.etree import XMLSchema
import pytest

from carbon_intensity.models.measurements import MeasurementResponse
from carbon_intensity.exceptions import APIConstraintException
from carbon_intensity.api import JSONClient, XMLClient
from ..conftest import today, yesterday


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityAfterDateAsJSON:
    def test_intensity_after(self, json_api: JSONClient):
        response = json_api.national.get_intensity_after(from_=today, days=1)
        assert isinstance(response, MeasurementResponse)

    def test_intensity_after_with_invalid_kwargs(self, json_api: JSONClient):
        with pytest.raises(APIConstraintException):
            json_api.national.get_intensity_after(from_=today, lustrums=1)

    def test_intensity_after_with_invalid_interval(self, json_api: JSONClient):
        with pytest.raises(ValidationError):
            json_api.national.get_intensity_after(from_=today, days=-1)


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityBeforeDateAsJSON:
    def test_intensity_before(self, json_api: JSONClient):
        response = json_api.national.get_intensity_before(from_=today, days=1)
        assert isinstance(response, MeasurementResponse)

    def test_intensity_before_with_invalid_kwargs(self, json_api: JSONClient):
        with pytest.raises(APIConstraintException):
            json_api.national.get_intensity_before(from_=today, lustrums=1)

    def test_intensity_before_with_invalid_interval(self, json_api: JSONClient):
        with pytest.raises(ValidationError):
            json_api.national.get_intensity_before(from_=today, days=-1)


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityBetweenDatesAsJSON:
    def test_intensity_between(self, json_api: JSONClient) -> None:
        response = json_api.national.get_intensity_between(from_=yesterday, to=today)
        assert isinstance(response, MeasurementResponse)

    def test_exception_with_same_dates(self, json_api: JSONClient) -> None:
        with pytest.raises(APIConstraintException):
            json_api.national.get_intensity_between(from_=today, to=today)

    def test_exception_with_invalid_interval(self, json_api: JSONClient) -> None:
        with pytest.raises(APIConstraintException):
            json_api.national.get_intensity_between(from_=today, to=yesterday)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityAfterDateAsXML:
    def test_intensity_after(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_after(from_=today, days=1)
        measurement_schema.assertValid(response.document)

    def test_intensity_after_with_invalid_kwargs(self, xml_api: XMLClient) -> None:
        with pytest.raises(APIConstraintException):
            xml_api.national.get_intensity_after(from_=today, lustrums=1)

    def test_intensity_after_with_invalid_interval(self, xml_api: XMLClient) -> None:
        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_after(from_=today, days=-1)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityBeforeDateAsXML:
    def test_intensity_before(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_before(from_=today, days=1)
        measurement_schema.assertValid(response.document)

    def test_intensity_before_with_invalid_kwargs(self, xml_api: XMLClient) -> None:
        with pytest.raises(APIConstraintException):
            xml_api.national.get_intensity_before(from_=today, lustrums=1)

    def test_intensity_before_with_invalid_interval(self, xml_api: XMLClient) -> None:
        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_before(from_=today, days=-1)


@pytest.mark.usefixtures("xml_api", "measurement_schema")
class TestNationalIntensityBetweenDatesAsXML:
    def test_intensity_between(
        self, xml_api: XMLClient, measurement_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_between(from_=yesterday, to=today)
        measurement_schema.assertValid(response.document)

    def test_exception_with_same_dates(self, xml_api: XMLClient) -> None:
        with pytest.raises(APIConstraintException):
            xml_api.national.get_intensity_between(from_=today, to=today)

    def test_exception_with_invalid_interval(self, xml_api: XMLClient) -> None:
        with pytest.raises(APIConstraintException):
            xml_api.national.get_intensity_between(from_=today, to=yesterday)
