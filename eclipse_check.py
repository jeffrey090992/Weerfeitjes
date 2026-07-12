import os
import requests
from datetime import datetime
import pytz

# --- Configuratie ---
WEBHOOK = os.getenv("DISCORD_WEBHOOK") # Zorg dat deze omgevingsvariabele is ingesteld
TZ = pytz.timezone("Europe/Amsterdam")
LAST_ALERT = "last_alert.txt"

def send_discord(message):
    if not WEBHOOK:
        print("Geen webhook gevonden. Stel de omgevingsvariabele 'DISCORD_WEBHOOK' in.")
        return
    try:
        response = requests.post(WEBHOOK, json={"content": message}, timeout=10)
        print("Discord melding verstuurd, status code:", response.status_code)
    except Exception as e:
        print(f"Fout bij versturen naar Discord: {e}")

def already_sent(event_id):
    if not os.path.exists(LAST_ALERT):
        return False
    with open(LAST_ALERT, "r") as f:
        return f.read().strip() == event_id

def save_sent(event_id):
    with open(LAST_ALERT, "w") as f:
        f.write(event_id)

def get_eclipse_data():
    return [
        {"id": "2026-08-12-solar", "type": "☀️ Zonsverduistering", "datetime": "2026-08-12 20:11", "visible": True},
        {"id": "2026-08-28-lunar", "type": "🌙 Maansverduistering", "datetime": "2026-08-28 05:13", "visible": True},
        {"id": "2027-02-20-lunar", "type": "🌙 Maansverduistering", "datetime": "2027-02-20 03:20", "visible": True},
        {"id": "2027-08-02-solar", "type": "☀️ Zonsverduistering", "datetime": "2027-08-02 17:40", "visible": True}
    ]

def check():
    now = datetime.now(TZ)
    eclipses = get_eclipse_data()

    for eclipse in eclipses:
        if not eclipse["visible"]:
            continue

        event_time = TZ.localize(datetime.strptime(eclipse["datetime"], "%Y-%m-%d %H:%M"))
        remaining = event_time - now

        # Controleer of de eclips binnen de komende 24 uur valt (maar nog niet voorbij is)
        if 0 < remaining.total_seconds() <= 86400:
            if already_sent(eclipse["id"]):
                continue # Melding is al verzonden

            message = (f"🚨 **Eclipse Alert Nederland 🇳🇱**\n\n"
                       f"{eclipse['type']}\n\n"
                       f"📅 Tijd: {event_time.strftime('%d-%m-%Y %H:%M')}\n"
                       f"📍 Zichtbaar: Nederland")
            
            send_discord(message)
            save_sent(eclipse["id"])
            return # Stop na het versturen van één melding

    print("Geen actuele eclips binnen 24 uur.")

if __name__ == "__main__":
    check()
