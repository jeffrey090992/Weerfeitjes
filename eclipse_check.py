import os
import requests
from datetime import datetime, timedelta
import pytz

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

TIMEZONE = pytz.timezone("Europe/Amsterdam")

# Nederlandse locatie (midden Nederland)
LOCATION = {
    "country": "Nederland",
    "visible": True
}

# Hier komen de astronomische gegevens binnen
# Later te vervangen door automatische NASA/JPL data
ECLIPSES = [
    {
        "id": "moon-2026-03-03",
        "type": "🌙 Maansverduistering",
        "date": datetime(2026, 3, 3, 12, 33)
    },
    {
        "id": "sun-2026-08-12",
        "type": "☀️ Zonsverduistering",
        "date": datetime(2026, 8, 12, 19, 47)
    }
]


def send_discord(message):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": message},
            timeout=10
        )


def already_sent(eclipse_id):
    if not os.path.exists("last_alert.txt"):
        return False

    with open("last_alert.txt") as file:
        return eclipse_id == file.read().strip()


def save_sent(eclipse_id):
    with open("last_alert.txt", "w") as file:
        file.write(eclipse_id)


def check():

    now = datetime.now()

    for eclipse in ECLIPSES:

        difference = eclipse["date"] - now

        if timedelta(0) < difference <= timedelta(hours=24):

            if not already_sent(eclipse["id"]):

                message = f"""
🚨 **Eclipse Alert Nederland 🇳🇱**

{eclipse['type']}

📅 Datum:
{eclipse['date'].strftime('%d-%m-%Y %H:%M')}

📍 Gebied:
Nederland

⏰ Nog:
{difference.seconds // 3600} uur

✅ Alleen zichtbaarheidscontrole Nederland
"""

                send_discord(message)
                save_sent(eclipse["id"])

            break


if __name__ == "__main__":
    check()
