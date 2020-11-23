from tests.base import BaseTestCase


class TestDefaultEndpoints(BaseTestCase):
    def test_current_intensity(self) -> None:
        response = self.api.get_current_intensity()
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_today_intensity(self) -> None:
        response = self.api.get_today_intensity()
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_intensity_factors(self) -> None:
        response = self.api.get_intensity_factors()
        is_valid = self.check_factors_schema(response)
        self.assertTrue(is_valid)
