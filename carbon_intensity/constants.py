BASE_URL = "https://api.carbonintensity.org.uk"

CURRENT_INTENSITY_URL = f"{BASE_URL}/intensity"
DAY_INTENSITY_URL = f"{BASE_URL}/intensity/date"
INTENSITY_FACTORS_URL = f"{BASE_URL}/intensity/factors"

MIN_PERIOD = 1
MAX_PERIOD = 48

ALLOWED_PENDULUM_ARGS = {
    "years",
    "months",
    "weeks",
    "days",
    "hours",
    "minutes",
    "seconds",
}
