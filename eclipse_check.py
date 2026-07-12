import os
import requests
from datetime import datetime, timedelta

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Nederlandse tijd
NU = datetime.now()

# Eclipsdata (UTC)
ECLIPSES = [
    {
        "type": "🌙 Maansverduistering",
        "datum": datetime(2026, 3, 3, 11, 33),
        "zichtbaar": True
    },
    {
        "type": "☀️ Zonsverduistering",
        "datum": datetime(2026, 8, 12, 17, 47),
        "zichtbaar": True
    }
]


def discord(tekst):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": tekst},
            timeout=10
        )


def controle():

    for eclipse in ECLIPSES:

        verschil = eclipse["datum"] - NU

        # melding 24 uur vooraf
        if timedelta(hours=23, minutes=50) < verschil < timedelta(hours=24, minutes=10):

            bericht = f"""
🚨 **Eclipse Alert Nederland**

{eclipse['type']}

📅 Datum:
{eclipse['datum'].strftime('%d-%m-%Y %H:%M')}

🇳🇱 Zichtbaar vanuit Nederland:
{"Ja" if eclipse['zichtbaar'] else "Nee"}

⏰ Dit is de 24 uur waarschuwing.
"""

            discord(bericht)

        elif verschil.days >= 0:
            print(
                f"{eclipse['type']} over {verschil.days} dagen"
            )


controle()
