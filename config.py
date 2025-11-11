# Import secrets from secrets.py
try:
    from .secrets import WIFI_SSID, WIFI_PASSWORD, TFL_APP_KEY
except ImportError:
    # Fallback to environment variables if secrets.py doesn't exist
    import os
    WIFI_SSID = os.getenv("WIFI_SSID", "")
    WIFI_PASSWORD = os.getenv("WIFI_PASSWORD", "")
    TFL_APP_KEY = os.getenv("TFL_APP_KEY", "")

# UI
MAX_PER_STOP = 4           # how many arrivals to show for each stop
UPDATE_INTERVAL = 10       # update interval (seconds)
