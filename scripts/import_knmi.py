import os
import pandas as pd

# Pad naar de root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
csv_path = os.path.join(root_dir, 'knmi_data.csv')

# --- JOUW DATA OPHAAL LOGICA ---
# VOORBEELD: Vervang dit door jouw daadwerkelijke ophaalcode
# df = pd.read_csv('...') of df = pd.DataFrame(...)
# ZORG DAT 'df' hier gevuld wordt met data!

# Controleer of df gevuld is
if 'df' in locals() and not df.empty:
    df.to_csv(csv_path, index=False)
    print(f"Bestand succesvol opgeslagen op {csv_path} met {len(df)} rijen.")
    aantal_records = len(df)
else:
    print("FOUT: 'df' is leeg of niet gedefinieerd!")
    exit(1)

# Output naar GitHub Actions
if 'GITHUB_OUTPUT' in os.environ:
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        fh.write(f"message=Succesvol {aantal_records} records opgehaald.\n")
