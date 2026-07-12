import os
import requests
from datetime import datetime, timedelta
import pytz
from skyfield.api import load, wgs84
from skyfield import almanac

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

tz = pytz.timezone("Europe/Amsterdam")

# Nederland (Amsterdam)
observer = wgs84.latlon(
    52.3676,
    4.9041
)

LAST_ALERT = "last_alert.txt"


def send_discord(message):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": message},
            timeout=10
        )


def already_sent(event):
    if not os.path.exists(LAST_ALERT):
        return False

    with open(LAST_ALERT) as f:
        return f.read().strip() == event


def save_sent(event):
    with open(LAST_ALERT, "w") as f:
        f.write(event)


def check():

    ts = load.timescale()
    eph = load("de421.bsp")

    now = datetime.now(tz)

    # komende periode bekijken
    start = ts.now()
    end = ts.utc(now.year + 2, 1, 1)

    t, events = almanac.find_discrete(
        start,
        end,
        almanac.eclipse_events(eph)
    )

    for time, event in zip(t, events):

        eclipse_time = time.utc_datetime().replace(
            tzinfo=pytz.utc
        ).astimezone(tz)

        verschil = eclipse_time - now

        if timedelta(0) < verschil <= timedelta(hours=24):

            if event == 0:
                soort = "☀️ Zonsverduistering"
            else:
                soort = "🌙 Maansverduistering"

            naam = f"{soort}-{eclipse_time}"

            if not already_sent(naam):

                bericht = f"""
🚨 **Eclipse Alert Nederland 🇳🇱**

{soort}

📅 Datum:
{eclipse_time.strftime('%d-%m-%Y %H:%M')}

📍 Controle locatie:
Nederland

⏰ Nog:
{verschil.seconds // 3600} uur

🔭 Astronomische berekening actief
"""

                send_discord(bericht)
                save_sent(naam)

            return

    print("Geen Nederlandse eclips binnen 24 uur")


if __name__ == "__main__":
    check()
