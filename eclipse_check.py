import os
import requests
from datetime import datetime, timedelta
import pytz
import json

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

TZ = pytz.timezone("Europe/Amsterdam")

LAST_ALERT = "last_alert.txt"

# Nederland
COUNTRY = "Netherlands"


def send_discord(message):
    if not WEBHOOK:
        print("Geen webhook gevonden")
        return

    response = requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )

    print("Discord:", response.status_code)


def already_sent(event_id):
    if not os.path.exists(LAST_ALERT):
        return False

    with open(LAST_ALERT) as f:
        return f.read().strip() == event_id


def save_sent(event_id):
    with open(LAST_ALERT, "w") as f:
        f.write(event_id)


def get_eclipse_data():

    # Officiële eclipskalendergegevens
    # Deze lijst bevat toekomstige eclipsen
    return [
        {
            "id": "2026-03-03-lunar",
            "type": "🌙 Maansverduistering",
            "datetime": "2026-03-03 12:33",
            "visible": True
        },
        {
            "id": "2026-08-12-solar",
            "type": "☀️ Zonsverduistering",
            "datetime": "2026-08-12 19:47",
            "visible": False
        }
    ]


def check():

    now = datetime.now(TZ)

    eclipses = get_eclipse_data()

    for eclipse in eclipses:

        if not eclipse["visible"]:
            continue

        event_time = TZ.localize(
            datetime.strptime(
                eclipse["datetime"],
                "%Y-%m-%d %H:%M"
            )
        )

        remaining = event_time - now

        if timedelta(0) < remaining <= timedelta(hours=24):

            if already_sent(eclipse["id"]):
                return

            message = f"""
🚨 **Eclipse Alert Nederland 🇳🇱**

{eclipse['type']}

📅 Tijd:
{event_time.strftime('%d-%m-%Y %H:%M')}

📍 Zichtbaar:
Nederland

⏰ Nog:
{remaining.seconds // 3600} uur
"""

            send_discord(message)

            save_sent(eclipse["id"])

            return

    print("Geen Nederlandse eclips binnen 24 uur")


if __name__ == "__main__":
    check()
