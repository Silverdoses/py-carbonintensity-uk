import pathlib

import requests_mock
import pytest

from carbon_intensity.exceptions import JSONClientException, XMLClientException
from carbon_intensity.constants import CURRENT_INTENSITY_URL, CURRENT_INTENSITY_URL_XML
from carbon_intensity.api import JSONClient, XMLClient
from ..conftest import current_path


@pytest.mark.usefixtures("json_api", "xml_api")
class TestClientExceptions:
    def test_json_api_failure(self, json_api: JSONClient):
        with open(f"{current_path}/templates/500.html") as page:
            html = page.read()

        with requests_mock.Mocker() as fake_adapter:
            fake_adapter.get(url=CURRENT_INTENSITY_URL, text=html)

            with pytest.raises(JSONClientException):
                json_api.national.get_current_intensity()

    def test_xml_api_failure(self, xml_api: XMLClient):
        with open(f"{current_path}/templates/500.html") as page:
            html = page.read()

        with requests_mock.Mocker() as fake_adapter:
            fake_adapter.get(url=CURRENT_INTENSITY_URL_XML, text=html)

            with pytest.raises(XMLClientException):
                xml_api.national.get_current_intensity()
