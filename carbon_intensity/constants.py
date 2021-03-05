BASE_URL = "https://api.carbonintensity.org.uk"

GENERATION_MIX_URL = f"{BASE_URL}/generation"

CURRENT_INTENSITY_URL = f"{BASE_URL}/intensity"
INTENSITY_BY_DATE_URL = f"{BASE_URL}/intensity/date"
INTENSITY_FACTORS_URL = f"{BASE_URL}/intensity/factors"
REGIONAL_INTENSITY_URL = f"{BASE_URL}/regional"

CURRENT_INTENSITY_URL_XML = f"{BASE_URL}/xml/intensity"
INTENSITY_BY_DATE_URL_XML = f"{BASE_URL}/xml/intensity/date"
INTENSITY_FACTORS_URL_XML = f"{BASE_URL}/xml/intensity/factors"
REGIONAL_INTENSITY_URL_XML = f"{BASE_URL}/xml/regional"

API_DATETIME_FORMAT = "%Y-%m-%dT%H:%MZ"
API_DATE_FORMAT = "%Y-%m-%d"

MIN_PERIOD = 1
MAX_PERIOD = 48

ALLOWED_COUNTRIES = ("england", "scotland", "wales")

ALLOWED_COUNTRIES_REGEX = rf"^({'|'.join(ALLOWED_COUNTRIES)}$)"

ALLOWED_PENDULUM_ARGS = {
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
}
