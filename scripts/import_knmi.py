import os
import pandas as pd

# Forceer het pad naar de root van de repository
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(root_dir, 'knmi_data.csv')

# --- JOUW BESTAANDE LOGICA ---
# Bijvoorbeeld: df = haal_data_op()
# df.to_csv(csv_path, index=False)

# Log het pad waar het bestand wordt opgeslagen
print(f"Opslaan van bestand naar: {csv_path}")

aantal_records = 5 
bericht = f"Succesvol {aantal_records} dagrecords geïmporteerd."

if 'GITHUB_OUTPUT' in os.environ:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f"message={bericht}\n")
