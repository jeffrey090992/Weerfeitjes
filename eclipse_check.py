import os
import requests
from datetime import datetime, timedelta
import pytz

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

TZ = pytz.timezone("Europe/Amsterdam")

LAST_ALERT = "last_alert.txt"

# NASA eclipse kalender (toekomstige eclipsen)
ECLIPSES = [
    {
        "id": "solar-2026-08-12",
        "type": "☀️ Zonsverduistering",
        "date": "2026-08-12 19:47",
        "netherlands": False
    },
    {
        "id": "lunar-2026-03-03",
        "type": "🌙 Maansverduistering",
        "date": "2026-03-03 12:33",
        "netherlands": True
    }
]


def send_discord(message):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": message},
            timeout=10
        )


def already_sent(event_id):
    if not os.path.exists(LAST_ALERT):
        return False

    with open(LAST_ALERT) as f:
        return f.read().strip() == event_id


def save_sent(event_id):
    with open(LAST_ALERT, "w") as f:
        f.write(event_id)


def check():

    now = datetime.now(TZ)

    for eclipse in ECLIPSES:

        if not eclipse["netherlands"]:
            continue

        event_time = TZ.localize(
            datetime.strptime(
                eclipse["date"],
                "%Y-%m-%d %H:%M"
            )
        )

        remaining = event_time - now

        if timedelta(0) < remaining <= timedelta(hours=24):

            if not already_sent(eclipse["id"]):

                message = f"""
🚨 **Eclipse Alert Nederland 🇳🇱**

{eclipse['type']}

📅 Datum:
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
