BASE_URL = "https://api.carbonintensity.org.uk"

# JSON API
GENERATION_MIX_URL = f"{BASE_URL}/generation"
CURRENT_INTENSITY_URL = f"{BASE_URL}/intensity"
INTENSITY_BY_DATE_URL = f"{BASE_URL}/intensity/date"
INTENSITY_FACTORS_URL = f"{BASE_URL}/intensity/factors"
REGIONAL_INTENSITY_URL = f"{BASE_URL}/regional"
INTENSITY_STATS_URL = f"{BASE_URL}/intensity/stats"

# XML API
CURRENT_INTENSITY_URL_XML = f"{BASE_URL}/xml/intensity"
INTENSITY_BY_DATE_URL_XML = f"{BASE_URL}/xml/intensity/date"
INTENSITY_FACTORS_URL_XML = f"{BASE_URL}/xml/intensity/factors"
REGIONAL_INTENSITY_URL_XML = f"{BASE_URL}/xml/regional"
INTENSITY_STATS_URL_XML = f"{BASE_URL}/xml/intensity/stats"

# Normalized API Date/Datetime formats
API_DATETIME_FORMAT = "%Y-%m-%dT%H:%MZ"
API_DATE_FORMAT = "%Y-%m-%d"

# Settlement period limits (Intensity by date)
MIN_PERIOD = 1
MAX_PERIOD = 48

# Intensity stats block limits
MIN_HOURS_BLOCK = 1
MAX_HOURS_BLOCK = 24

# Regional endpoints (Beta)
ALLOWED_REGIONS = ("england", "scotland", "wales")
ALLOWED_REGIONS_REGEX = rf"^({'|'.join(ALLOWED_REGIONS)}$)"

# Allowed intervals to (before/after)-date-based endpoints.
ALLOWED_PENDULUM_ARGS = {
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
}
