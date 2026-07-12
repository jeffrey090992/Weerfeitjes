import os
import requests
from datetime import datetime, timedelta

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

ECLIPSES = [
    {
        "id": "2026-03-03-moon",
        "type": "🌙 Maansverduistering",
        "datum": datetime(2026, 3, 3, 11, 33),
        "locatie": "Nederland"
    },
    {
        "id": "2026-08-12-sun",
        "type": "☀️ Zonsverduistering",
        "datum": datetime(2026, 8, 12, 17, 47),
        "locatie": "Nederland"
    }
]


def stuur_discord(bericht):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": bericht},
            timeout=10
        )


def al_gemeld(eclipse_id):
    if not os.path.exists("last_alert.txt"):
        return False

    with open("last_alert.txt") as f:
        return f.read().strip() == eclipse_id


def opslaan(eclipse_id):
    with open("last_alert.txt", "w") as f:
        f.write(eclipse_id)


def controle():

    nu = datetime.now()

    for eclipse in ECLIPSES:

        verschil = eclipse["datum"] - nu

        # Alleen melden tussen 24 en 0 uur vooraf
        if timedelta(0) < verschil <= timedelta(hours=24):

            if not al_gemeld(eclipse["id"]):

                bericht = f"""
🚨 **Astronomie waarschuwing Nederland**

{eclipse['type']} komt eraan!

📅 Tijd:
{eclipse['datum'].strftime('%d-%m-%Y %H:%M')}

📍 Locatie:
🇳🇱 {eclipse['locatie']}

⏰ Nog ongeveer:
{verschil.days} dagen en {verschil.seconds//3600} uur
"""

                stuur_discord(bericht)
                opslaan(eclipse["id"])

            return

    print("Geen komende verduistering binnen 24 uur.")


controle()
