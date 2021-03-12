import pytest
from pydantic import ValidationError

from carbon_intensity.api import JSONClient
from carbon_intensity.exceptions import APIConstraintException
from ..conftest import yesterday, today
from carbon_intensity.models.mixes import (GenerationMixResponse,
                                           GenerationMixListResponse)


@pytest.mark.usefixtures("json_api")
class TestNationalGenerationMixAsJSON:
    def test_current_generation_mix(self, json_api: JSONClient):
        response = json_api.national.get_current_generation_mix()
        assert isinstance(response, GenerationMixResponse)


@pytest.mark.usefixtures("json_api")
class TestNationalGenerationMixBeforeDateAsJSON:
    def test_generation_mix_before(self, json_api: JSONClient):
        response = json_api.national.get_generation_mix_before(from_=today, days=1)
        assert isinstance(response, GenerationMixListResponse)

    def test_generation_mix_with_invalid_kwargs(self, json_api: JSONClient):
        with pytest.raises(APIConstraintException):
            json_api.national.get_generation_mix_before(from_=today, lustrums=1)

    def test_generation_mix_with_invalid_interval(self, json_api: JSONClient):
        with pytest.raises(ValidationError):
            json_api.national.get_generation_mix_before(from_=today, days=-1)


@pytest.mark.usefixtures('json_api')
class TestNationalGenerationMixBetweenDatesAsJSON:
    def test_generation_mix_between(self, json_api: JSONClient) -> None:
        response = json_api.national.get_generation_mix_between(
            from_=yesterday,
            to=today
        )
        assert isinstance(response, GenerationMixListResponse)

    def test_exception_with_same_dates(self, json_api: JSONClient) -> None:
        with pytest.raises(APIConstraintException):
            json_api.national.get_generation_mix_between(from_=today, to=today)

    def test_exception_with_invalid_interval(self, json_api: JSONClient) -> None:
        with pytest.raises(APIConstraintException):
            json_api.national.get_generation_mix_between(from_=today, to=yesterday)