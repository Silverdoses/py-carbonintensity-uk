import pytest
import random

from lxml.etree import XMLSchema
from pydantic import ValidationError

from carbon_intensity.models.stats import StatsListResponse
from carbon_intensity.api import JSONClient, XMLClient
from carbon_intensity.constants import MIN_HOURS_BLOCK, MAX_HOURS_BLOCK
from ..conftest import today, yesterday


@pytest.mark.usefixtures("json_api")
class TestNationalIntensityStatsAsJSON:
    def test_intensity_stats_between(self, json_api: JSONClient) -> None:
        response = json_api.national.get_intensity_stats_between(
            from_=yesterday, to=today
        )
        assert isinstance(response, StatsListResponse)

    def test_intensity_stats_between_with_block(self, json_api: JSONClient) -> None:
        hours_block = random.randrange(MIN_HOURS_BLOCK, MAX_HOURS_BLOCK)
        response = json_api.national.get_intensity_stats_between(
            from_=yesterday, to=today, block=hours_block
        )
        assert isinstance(response, StatsListResponse)

    def test_exception_with_invalid_lesser_block(self, json_api: JSONClient) -> None:
        with pytest.raises(ValidationError):
            json_api.national.get_intensity_stats_between(
                from_=yesterday, to=today, block=MIN_HOURS_BLOCK - 1
            )

    def test_exception_with_invalid_greater_block(self, json_api: JSONClient) -> None:
        with pytest.raises(ValidationError):
            json_api.national.get_intensity_stats_between(
                from_=yesterday, to=today, block=MAX_HOURS_BLOCK + 1
            )


@pytest.mark.usefixtures("xml_api", "stats_schema")
class TestNationalIntensityStatsAsXML:
    def test_intensity_stats_between(
        self, xml_api: XMLClient, stats_schema: XMLSchema
    ) -> None:
        response = xml_api.national.get_intensity_stats_between(
            from_=yesterday, to=today
        )
        stats_schema.assertValid(response.document)

    def test_intensity_stats_between_with_block(
        self, xml_api: XMLClient, stats_schema: XMLSchema
    ) -> None:
        hours_block = random.randrange(MIN_HOURS_BLOCK, MAX_HOURS_BLOCK)
        response = xml_api.national.get_intensity_stats_between(
            from_=yesterday, to=today, block=hours_block
        )
        stats_schema.assertValid(response.document)

    def test_exception_with_invalid_lesser_block(self, xml_api: XMLClient) -> None:
        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_stats_between(
                from_=yesterday, to=today, block=MIN_HOURS_BLOCK - 1
            )

    def test_exception_with_invalid_greater_block(self, xml_api: XMLClient) -> None:
        with pytest.raises(ValidationError):
            xml_api.national.get_intensity_stats_between(
                from_=yesterday, to=today, block=MAX_HOURS_BLOCK + 1
            )
