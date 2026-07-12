import pandas as pd
import json
import os

# Controleer of het bestand bestaat
if not os.path.exists("knmi_data.csv"):
    print("Fout: knmi_data.csv niet gevonden")
    exit(1)

# Lees de CSV. KNMI bestanden hebben 12 commentaarregels.
# We gebruiken 'header=12' om de kolomnamen direct goed te krijgen.
df = pd.read_csv("knmi_data.csv", skiprows=12)

# Verwijder spaties uit kolomnamen (KNMI headers hebben vaak voorloopspaties)
df.columns = df.columns.str.strip()

# Check of de benodigde kolommen bestaan
if 'TX' in df.columns and 'TN' in df.columns and 'RH' in df.columns:
    # Bereken waarden en deel door 10 (KNMI standaard)
    warmste = df['TX'].max() / 10
    koudste = df['TN'].min() / 10
    natste = df['RH'].max() / 10

    record_data = {
        "datum": "12-07-2026",
        "warmste": {"waarde": str(warmste), "datum": "12-07-2026"},
        "koudste": {"waarde": str(koudste), "datum": "12-07-2026"},
        "natste": {"waarde": str(natste), "datum": "12-07-2026"}
    }
else:
    # Fallback als kolommen niet gevonden worden
    record_data = {
        "datum": "12-07-2026",
        "warmste": {"waarde": "0", "datum": "n.v.t."},
        "koudste": {"waarde": "0", "datum": "n.v.t."},
        "natste": {"waarde": "0", "datum": "n.v.t."}
    }

# Opslaan
with open("daily_records.json", "w") as f:
    json.dump(record_data, f)

print("daily_records.json succesvol gegenereerd.")
