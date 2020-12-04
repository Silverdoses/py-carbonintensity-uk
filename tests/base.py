import unittest
from typing import Dict

from carbon_intensity.api import UKCarbonAPI


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.api = UKCarbonAPI()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api.close()

    def check_intensity_schema(self, response: Dict) -> bool:
        self.assertIn("data", response, msg="Schema must contain data key")

        record = response["data"]
        self.assertIsInstance(record, list, msg="Data must be an array")
        self.assertGreaterEqual(len(record), 1)

        measurement = record[0]
        self.assertTrue({"from", "to", "intensity"}.issubset(measurement.keys()))

        intensity = measurement["intensity"]
        self.assertTrue({"forecast", "actual", "index"}.issubset(intensity.keys()))
        self.assertIsInstance(intensity["forecast"], int)
        self.assertIn(type(intensity["actual"]), (int, type(None)))
        self.assertIsInstance(intensity["index"], str)

        return True

    def check_intensity_empty_schema(self, response: Dict) -> bool:
        self.assertIn("data", response, msg="Schema must contain data key")

        record = response["data"]
        self.assertIsInstance(record, list, msg="Data must be an array")
        self.assertEqual(len(record), 0)

        return True

    def check_factors_schema(self, response: Dict) -> bool:
        self.assertIn("data", response)

        record = response["data"]
        self.assertIsInstance(record, list)
        self.assertEqual(len(record), 1, msg="Response must contains only one record")

        factors = record[0]
        self.assertIsInstance(factors, dict)
        self.assertGreaterEqual(len(factors.keys()), 1)

        return True
