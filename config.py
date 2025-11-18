# Import secrets from secrets.py
import secrets
WIFI_SSID = secrets.WIFI_SSID
WIFI_PASSWORD = secrets.WIFI_PASSWORD
TFL_APP_KEY = secrets.TFL_APP_KEY

# UI
MAX_PER_STOP = 4           # how many arrivals to show for each stop
UPDATE_INTERVAL = 60       # update interval (seconds)

# Bus stop IDs to monitor
BUS_STOPS = [
    {"id": "490016290W", "showName": True, "showDestination": True, "showCountdown": True},
    {"id": "490016290E", "showName": True, "showDestination": True, "showCountdown": True},
    
]
# 490007176N
# 490007176S