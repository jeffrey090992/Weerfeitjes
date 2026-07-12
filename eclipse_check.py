import os
import requests
from datetime import datetime

webhook = os.getenv("DISCORD_WEBHOOK")

def send_discord(message):
    if webhook:
        requests.post(
            webhook,
            json={"content": message},
            timeout=10
        )

# Tijdelijke testmelding
# Wordt later vervangen door echte astronomische berekening

bericht = f"""
🌙☀️ Eclipse Check Nederland

De controle is uitgevoerd:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

Locatie:
🇳🇱 Nederland

"""

send_discord(bericht)

print("Eclipse controle uitgevoerd")
