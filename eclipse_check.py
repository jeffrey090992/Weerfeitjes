import os
import requests
from datetime import datetime

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Voorbeeld: NASA eclipse API endpoint (vervang eventueel door eigen bron)
API_URL = "https://eclipse.gsfc.nasa.gov/SEsearch/SEsearchmap.php"

def stuur_discord(bericht):
    if WEBHOOK:
        requests.post(
            WEBHOOK,
            json={"content": bericht},
            timeout=10
        )

def controleer_eclipse():

    vandaag = datetime.now().strftime("%d-%m-%Y")

    # Hier kun je later echte berekening toevoegen
    # Voor nu demo-resultaat:
    eclipse = False

    if eclipse:
        bericht = f"""
🌙☀️ **Verduistering zichtbaar in Nederland!**

Datum:
{vandaag}

Locatie:
🇳🇱 Nederland

Controle:
{datetime.now().strftime("%H:%M")}
"""
        stuur_discord(bericht)

    else:
        print("Geen verduistering gevonden")


controleer_eclipse()
