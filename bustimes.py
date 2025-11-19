# ICON bus
# NAME Bus Times
# DESC Shows live TfL bus arrivals

import time
import math
import urequests as requests
import ntptime
from presto import Presto
import config

# --- Setup ---
presto = Presto()
display = presto.display
WIDTH, HEIGHT = display.get_bounds()

# region Set up colours
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
GREEN = display.create_pen(0, 255, 0)
BLUE = display.create_pen(0, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
ORANGE = display.create_pen(255, 165, 0)
PURPLE = display.create_pen(128, 0, 128)
PINK = display.create_pen(255, 192, 203)
LIME = display.create_pen(50, 205, 50)
NAVY = display.create_pen(0, 0, 128)
TEAL = display.create_pen(0, 128, 128)
GREY = display.create_pen(128, 128, 128)
BROWN = display.create_pen(139, 69, 19)
# endregion

BASE_URL = "https://api.tfl.gov.uk"


# --- Helper functions ---
def show_message(text, colour=WHITE):
    display.set_pen(BLACK)
    display.clear()
    display.set_pen(colour)
    display.text(str(text), 5, 10, WIDTH, 2)
    presto.update()


def show_status(text, colour=WHITE):
    display.set_pen(colour)
    display.text(str(text), 0, HEIGHT - 20, WIDTH, 1)
    presto.update()


def wifi_connect():
    show_status("Connecting Wi-Fi...")
    try:
        presto.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    except Exception as e:
        show_status("Wi-Fi error:\n" + str(e))
        while True:
            time.sleep(1)


def fetch_arrivals(stop_id):
    url = f"{BASE_URL}/stoppoint/{stop_id}/arrivals?app_key={config.TFL_APP_KEY}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            data.sort(key=lambda a: a.get("timeToStation", 99999))
            return data
        else:
            return []
    except Exception as e:
        print("fetch error:", e)
        return []
    finally:
        try:
            r.close()
        except:
            pass


def minutes_from_seconds(s):
    if s < 30:
        return "due"
    return f"{math.floor(s/60)}"


def draw_arrivals(stopData):
    display.set_pen(BLACK)
    display.clear()
    y = 10

    if not stopData:
        display.set_pen(WHITE)
        display.text("No data", 10, y, WIDTH, 2)
        presto.update()
        return

    for s in stopData:
        arrivals = s.get("arrivals", [])
        display.set_pen(RED)
        display.text(s.get("stopId", "Bus Stop"), 10, y, WIDTH, 2)
        y += 25
        for a in arrivals[: config.MAX_PER_STOP]:
            line = a.get("lineName", "?")
            stop = a.get("platformName", "")
            dest = a.get("destinationName", "").split(" - ")[0]
            mins = minutes_from_seconds(a.get("timeToStation", 0))
            text = f"{line} {dest[:16]} {mins}"
            display.set_pen(WHITE)
            display.text(text, 10, y, WIDTH, 2)
            y += 20

    presto.update()


# --- Main logic ---
wifi_connect()

try:
    ntptime.settime()
except OSError:
    show_message("Could not sync time")

while True:
    stopData = []
    for bus in config.BUS_STOPS:
        show_status("Fetching buses...")
        arrivals = fetch_arrivals(bus["id"])
        stopName = arrivals[0]["platformName"] if arrivals else naptan
        stopData.append({"stopId": stopName, "arrivals": arrivals})
    display.set_pen(BLACK)
    display.clear()
    draw_arrivals(stopData)
    time.sleep(config.UPDATE_INTERVAL)
