from typing import Dict, Optional
import json

from lxml.etree import _Element
from lxml import etree
import xmltodict


class XMLResponse:
    def __init__(self, element: _Element):
        self.document = element

    def save_to_file(self, path: str, encoding: Optional[str] = "utf-8") -> None:
        with open(path, mode="w", encoding=encoding) as file:
            file.write(self.to_string(encoding))

    def to_string(self, encoding: Optional[str] = "utf-8") -> str:
        return etree.tostring(
            self.document, encoding=encoding, pretty_print=True
        ).decode(encoding)

    def to_dict(self) -> Dict:
        return xmltodict.parse(self.to_string())

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
