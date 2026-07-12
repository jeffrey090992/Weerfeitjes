import os
import requests
from datetime import datetime, timedelta
import pytz

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

AMSTERDAM = pytz.timezone("Europe/Amsterdam")

# Nederlandse zichtbare eclipsen
# Wordt later vervangen door automatische astronomische data
ECLIPSES = [
    {
        "id": "moon-2026-03-03",
        "type": "🌙 Maansverduistering",
        "date": "2026-03-03 12:33",
        "visible": True
    },
    {
        "id": "sun-2026-08-12",
        "type": "☀️ Zonsverduistering",
        "date": "2026-08-12 19:47",
        "visible": True
    }
]


def send_discord(message):
    if not WEBHOOK:
        print("Geen Discord webhook gevonden")
        return

    response = requests.post(
        WEBHOOK,
        json={"content": message},
        timeout=10
    )

    print("Discord status:", response.status_code)


def load_last_alert():
    if os.path.exists("last_alert.txt"):
        with open("last_alert.txt") as f:
            return f.read().strip()

    return ""


def save_last_alert(eclipse_id):
    with open("last_alert.txt", "w") as f:
        f.write(eclipse_id)


def check_eclipse():

    now = datetime.now(AMSTERDAM)

    last_alert = load_last_alert()

    for eclipse in ECLIPSES:

        eclipse_time = AMSTERDAM.localize(
            datetime.strptime(
                eclipse["date"],
                "%Y-%m-%d %H:%M"
            )
        )

        verschil = eclipse_time - now

        # Alleen Nederland + alleen 24 uur vooraf
        if (
            eclipse["visible"]
            and timedelta(0) < verschil <= timedelta(hours=24)
        ):

            if last_alert != eclipse["id"]:

                bericht = f"""
🚨 **Eclipse Alert Nederland 🇳🇱**

{eclipse['type']}

📅 Datum:
{eclipse_time.strftime('%d-%m-%Y %H:%M')}

📍 Zichtbaar:
Nederland

⏰ Nog:
{verschil.seconds // 3600} uur

🔭 Automatische controle actief
"""

                send_discord(bericht)
                save_last_alert(eclipse["id"])

            else:
                print("Melding al verstuurd")

            return

    print("Geen Nederlandse eclips binnen 24 uur")


if __name__ == "__main__":
    check_eclipse()
