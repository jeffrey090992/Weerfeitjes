import os
import requests
from datetime import datetime

webhook = os.getenv("DISCORD_WEBHOOK")

bericht = f"""
🌙☀️ Eclipse Check Nederland

Controle uitgevoerd:
{datetime.now().strftime("%d-%m-%Y %H:%M")}

Locatie:
🇳🇱 Nederland
"""

if webhook:
    requests.post(
        webhook,
        json={"content": bericht},
        timeout=10
    )

print("Eclipse controle uitgevoerd")
