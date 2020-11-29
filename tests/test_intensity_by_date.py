import random

import pendulum

from carbon_intensity.exceptions import APITypeError, APIConstraintException
from carbon_intensity.constants import MIN_PERIOD, MAX_PERIOD
from tests.base import BaseTestCase


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


class TestIntensityByDateWithPeriod(BaseTestCase):
    def test_with_minimum_period(self):
        today = pendulum.now()
        response = self.api.get_intensity_by_date(date=today, period=MIN_PERIOD)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_maximum_period(self):
        today = pendulum.now()
        response = self.api.get_intensity_by_date(date=today, period=MAX_PERIOD)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)

    def test_with_random_valid_period(self):
        today = pendulum.now()
        period = random.randrange(MIN_PERIOD, MAX_PERIOD)
        response = self.api.get_intensity_by_date(date=today, period=period)
        is_valid = self.check_intensity_schema(response)
        self.assertTrue(is_valid)


class TestIntensityByDateValidations(BaseTestCase):
    def test_with_wrong_string_format(self):
        invalid_date = "1234-56-78"

        with self.assertRaises(APITypeError):
            self.api.get_intensity_by_date(date=invalid_date)

    def test_with_wrong_period_value(self):
        lesser_than_limit = MIN_PERIOD - 1
        greater_than_limit = MAX_PERIOD + 1
        today = pendulum.now()

        with self.assertRaises(APIConstraintException):
            self.api.get_intensity_by_date(date=today, period=lesser_than_limit)

        with self.assertRaises(APIConstraintException):
            self.api.get_intensity_by_date(date=today, period=greater_than_limit)

    def test_with_wrong_period_types(self):
        args = ['Non-integer string', b'Non-integer bytes']
        today = pendulum.now()

        for arg in args:
            with self.subTest(arg=arg):
                with self.assertRaises(APITypeError):
                    self.api.get_intensity_by_date(date=today, period=arg)

    def test_with_wrong_date_types(self):
        args = [True, False, list(), tuple(), dict(), set()]

        for arg in args:
            with self.subTest(arg=arg):
                with self.assertRaises(APITypeError):
                    self.api.get_intensity_by_date(date=arg)
