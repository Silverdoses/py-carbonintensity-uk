import pathlib

from lxml.etree import XMLSchema
from lxml import etree
import pendulum
import pytest

from carbon_intensity.api import JSONClient, XMLClient

current_path = pathlib.Path(__file__).parent.absolute()

# Dates for testing
today = pendulum.now(tz="UTC")
yesterday = today.subtract(days=1)
tomorrow = today.add(days=1)


@pytest.fixture(scope="class")
def json_api() -> JSONClient:
    """
    Sets up a client to communicate with UK Carbon Intensity API
    using JSON as the response format.
    """
    return JSONClient()


@pytest.fixture(scope="class")
def xml_api() -> XMLClient:
    """
    Sets up a client to communicate with UK Carbon Intensity API
    using XML structure as the response format.
    """
    return XMLClient()


@pytest.fixture(scope="class")
def measurement_schema() -> XMLSchema:
    """
    Sets up the Measurement XML schema to validate responses
    from the XML API
    """
    return XMLSchema(etree.parse(f"{current_path}/schemas/measurement.xsd"))


@pytest.fixture(scope="class")
def factors_schema() -> XMLSchema:
    """
    Sets up the Factors XML schema to validate responses
    from the XML API
    """
    return XMLSchema(etree.parse(f"{current_path}/schemas/factors.xsd"))


@pytest.fixture(scope="class")
def stats_schema() -> XMLSchema:
    """
    Sets up the Stats XML schema to validate responses
    from the XML API
    """
    return XMLSchema(etree.parse(f"{current_path}/schemas/stats.xml"))
