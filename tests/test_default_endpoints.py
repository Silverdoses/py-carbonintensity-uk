from carbon_intensity.api import UKCarbonAPI
import unittest


class TestDefaultEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.api = UKCarbonAPI()

    def tearDown(self) -> None:
        self.api.close()

    def test_current_intensity(self) -> None:
        measurement = self.api.get_current_intensity()
        self.assertIn("data", measurement, msg="Response does not contain data key")
        record = measurement["data"]
        self.assertIs(type(record), list, msg="Response has unknown schema")
        self.assertEqual(
            len(record), 1, msg="Response must contains only one measurement"
        )

    def test_today_intensity(self) -> None:
        measurement = self.api.get_today_intensity()
        self.assertIn("data", measurement, msg="Response does not contain data key")
        record = measurement["data"]
        self.assertIs(type(record), list, msg="Response has unknown schema")
        self.assertGreaterEqual(
            len(record), 1, msg="Response must contains at least one measurement"
        )

    def test_intensity_factors(self) -> None:
        information = self.api.get_intensity_factors()
        self.assertIn("data", information, msg="Response does not contain data key")
        record = information["data"]
        self.assertIs(type(record), list, msg="Response has unknown schema")
        self.assertEqual(len(record), 1, msg="Response must contains only one record")
        factors = record[0]
        self.assertIs(type(factors), dict, msg="Response has unknown schema")
        self.assertGreaterEqual(
            len(factors.keys()), 1, msg="API did not return any factors"
        )
