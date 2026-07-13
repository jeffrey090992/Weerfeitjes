import os
import json
import pandas as pd

# Directe verwijzing naar de root, aangezien de Action vanuit de root draait
csv_path = 'knmi_data.csv'

if not os.path.exists(csv_path):
    print(f"Fout: {csv_path} niet gevonden in {os.getcwd()}")
    exit(1)

df = pd.read_csv(csv_path)

# --- JOUW VERWERKINGSLOGICA ---
# Hier wordt daily_records.json aangemaakt in de root
# voorbeeld: resultaat.to_json('daily_records.json')
