import pendulum

from tests.base import BaseTestCase
from carbon_intensity.exceptions import APITypeError


class TestIntensityByDate(BaseTestCase):
    def test_with_past_date(self):
        one_week_ago = pendulum.now().subtract(weeks=1)
        response = self.api.get_intensity_by_date(date=one_week_ago)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_past_date_as_string(self):
        one_week_ago = pendulum.now().subtract(weeks=1).strftime("%Y-%m-%d")
        response = self.api.get_intensity_by_date(date=one_week_ago)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_current_date(self):
        today = pendulum.now()
        response = self.api.get_intensity_by_date(date=today)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_current_date_as_string(self):
        today = pendulum.now().strftime("%Y-%m-%d")
        response = self.api.get_intensity_by_date(date=today)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_future_date(self):
        one_week_later = pendulum.now().add(weeks=1)
        response = self.api.get_intensity_by_date(date=one_week_later)
        is_valid = self.check_intensity_empty_schema(response)
        self.assertTrue(is_valid)

    def test_with_future_date_as_string(self):
        one_week_later = pendulum.now().add(weeks=1).strftime("%Y-%m-%d")
        response = self.api.get_intensity_by_date(date=one_week_later)
        is_valid = self.check_intensity_empty_schema(response)
        self.assertTrue(is_valid)


class TestIntensityByDateValidations(BaseTestCase):
    def test_with_wrong_string_format(self):
        invalid_date = "1234-56-78"

        with self.assertRaises(APITypeError):
            self.api.get_intensity_by_date(date=invalid_date)

    def test_with_wrong_types(self):
        args = [True, False, list(), tuple(), dict(), set()]

        for arg in args:
            with self.subTest(arg=arg):
                with self.assertRaises(APITypeError):
                    self.api.get_intensity_by_date(date=arg)
