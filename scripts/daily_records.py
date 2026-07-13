import os
import json
import pandas as pd

# Pad naar de data in de root
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, 'knmi_data.csv')

if not os.path.exists(csv_path):
    print("Fout: knmi_data.csv niet gevonden")
    exit(1)

# --- JOUW VERWERKINGSLOGICA ---
# Hier wordt je data ingelezen en daily_records.json aangemaakt
