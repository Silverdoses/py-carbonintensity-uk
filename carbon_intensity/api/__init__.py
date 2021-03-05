from typing import Any

import requests

from .national import NationalJSONAPI, NationalXMLAPI
from .regional import RegionalJSONAPI


class JSONClient:
    def __init__(self, **kwargs: Any):
        self.session = requests.Session()
        self._settings = {"session": self.session, **kwargs}
        self.national = NationalJSONAPI(**self._settings)
        self.regional = RegionalJSONAPI(**self._settings)


class XMLClient:
    def __init__(self, **kwargs):
        self.session = requests.Session()
        self.national = NationalXMLAPI(self.session, **kwargs)
