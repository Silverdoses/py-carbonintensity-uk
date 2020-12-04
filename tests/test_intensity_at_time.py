import pendulum

from carbon_intensity.exceptions import APITypeError
from carbon_intensity.constants import API_DATETIME_FORMAT
from tests.base import BaseTestCase


class TestIntensityAtTime(BaseTestCase):
    def test_with_current_datetime(self):
        now = pendulum.now()
        response = self.api.get_intensity_at_time(time=now)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_past_datetime(self):
        one_week_ago = pendulum.now().subtract(weeks=1)
        response = self.api.get_intensity_at_time(time=one_week_ago)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_future_datetime(self):
        one_week_later = pendulum.now().add(weeks=1)
        response = self.api.get_intensity_at_time(time=one_week_later)
        is_valid = self.check_intensity_empty_schema(response)
        self.assertTrue(is_valid)


class TestIntensityAtTimeAsString(BaseTestCase):
    def test_with_current_datetime_default(self):
        now = pendulum.now().strftime(API_DATETIME_FORMAT)
        response = self.api.get_intensity_at_time(time=now)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_past_datetime_default(self):
        one_week_ago = pendulum.now().subtract(weeks=1).strftime(API_DATETIME_FORMAT)
        response = self.api.get_intensity_at_time(time=one_week_ago)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_future_datetime_default(self):
        one_week_later = pendulum.now().add(weeks=1).strftime(API_DATETIME_FORMAT)
        response = self.api.get_intensity_at_time(time=one_week_later)
        is_valid = self.check_intensity_empty_schema(response)
        self.assertTrue(is_valid)

    def test_with_current_datetime_iso8601(self):
        now = pendulum.now().to_iso8601_string()
        response = self.api.get_intensity_at_time(time=now)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_past_datetime_iso8601(self):
        one_week_ago = pendulum.now().subtract(weeks=1).to_iso8601_string()
        response = self.api.get_intensity_at_time(time=one_week_ago)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_future_datetime_iso8601(self):
        one_week_later = pendulum.now().add(weeks=1).to_iso8601_string()
        response = self.api.get_intensity_at_time(time=one_week_later)
        is_valid = self.check_intensity_empty_schema(response)
        self.assertTrue(is_valid)


class TestIntensityAtTimeValidations(BaseTestCase):
    def test_with_invalid_date_string(self):
        invalid_date = "1234-56-78"

        with self.assertRaises(APITypeError):
            self.api.get_intensity_at_time(time=invalid_date)

    def test_with_wrong_date_types(self):
        args = [100, True, None, list(), dict()]

        for arg in args:
            with self.subTest(arg=arg):
                with self.assertRaises(APITypeError):
                    self.api.get_intensity_at_time(time=arg)
