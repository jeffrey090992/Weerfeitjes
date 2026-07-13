import os
import pandas as pd

# 1. Definieer het pad
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(root_dir, 'knmi_data.csv')

# 2. HIER MOET JOUW LOGICA STAAN OM DATA TE HALEN
# Zorg dat je 'df' definieert. Bijvoorbeeld:
# df = pd.read_csv('jouw_bron_url_of_bestand') 
# OF als je zelf data maakt:
# df = pd.DataFrame({'datum': ['2026-07-13'], 'waarde': [20]})

# Controleer of df bestaat voordat we opslaan
if 'df' in locals():
    df.to_csv(csv_path, index=False)
    print(f"Opslaan van bestand naar: {csv_path}")
    aantal_records = len(df)
else:
    # Als df niet bestaat, maak een lege dummy om de fout te voorkomen
    df = pd.DataFrame()
    print("Waarschuwing: df was niet gedefinieerd, lege file aangemaakt.")
    df.to_csv(csv_path, index=False)
    aantal_records = 0

# 3. Output naar GitHub
bericht = f"Succesvol {aantal_records} dagrecords geïmporteerd."

if 'GITHUB_OUTPUT' in os.environ:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f"message={bericht}\n")
