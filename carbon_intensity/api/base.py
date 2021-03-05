from typing import Dict

from lxml.etree import _Element
from requests import Session
from lxml import etree

from ..exceptions import JSONClientException, XMLClientException


class BaseAPI:
    def __init__(self, session: Session, session_kwargs: Dict):
        self.session = session
        self.session_kwargs = session_kwargs

    def _request_as_json(self, method: str, **kwargs) -> Dict:
        request_method = getattr(self.session, method)
        settings = {**kwargs, **self.session_kwargs}

        try:
            response = request_method(**settings).json()
        except Exception as e:
            raise JSONClientException(e)

        return response

    def _request_as_xml(self, method: str, **kwargs) -> _Element:
        request_method = getattr(self.session, method)
        settings = {**kwargs, **self.session_kwargs}

        try:
            response = request_method(**settings)
            document = etree.fromstring(response.content)
        except Exception as e:
            raise XMLClientException(e)

        return document
