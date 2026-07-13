import os
import pandas as pd

# --- JOUW BESTAANDE LOGICA ---
# df.to_csv('knmi_data.csv', index=False)
aantal_records = 5 
bericht = f"Succesvol {aantal_records} dagrecords geïmporteerd."

# --- OUTPUT NAAR GITHUB ---
if 'GITHUB_OUTPUT' in os.environ:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f"message={bericht}\n")

print(f"Status: 200")
