import pytest

from carbon_intensity.api import JSONClient


@pytest.mark.usefixtures("json_api")
class TestNationalPandasIntegration:
    def test_intensity_response_to_dataframe(self, json_api: JSONClient):
        response = json_api.national.get_current_intensity()
        expected_columns = {
            'from',
            'to',
            'actual',
            'forecast',
            'index'
        }
        dataframe = response.to_dataframe()
        assert expected_columns.issubset(dataframe.columns)

    def test_intensity_factor_response_to_dataframe(self, json_api: JSONClient):
        response = json_api.national.get_intensity_factors()
        expected_columns = {
            'biomass',
            'coal',
            'dutch_imports',
            'french_imports',
            'gas_combined_cycle',
            'gas_open_cycle',
            'hydro',
            'irish_imports',
            'nuclear',
            'oil',
            'other',
            'pumped_storage',
            'solar',
            'wind'
        }
        dataframe = response.to_dataframe()
        assert expected_columns.issubset(dataframe.columns)
