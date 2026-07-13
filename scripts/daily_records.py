import os
import json
import pandas as pd

# Forceer hetzelfde pad naar de root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(root_dir, 'knmi_data.csv')

if not os.path.exists(csv_path):
    print(f"FOUT: Bestand niet gevonden op {csv_path}")
    exit(1)

df = pd.read_csv(csv_path)

# --- JOUW VERWERKINGSLOGICA ---
# Sla daily_records.json ook in de root op
json_path = os.path.join(root_dir, 'daily_records.json')
# resultaat.to_json(json_path)
