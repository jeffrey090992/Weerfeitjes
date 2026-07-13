import os

# --- JOUW BESTAANDE LOGICA HIER ---
# Voorbeeld:
aantal_records = 5 
bericht = f"Succesvol {aantal_records} dagrecords geïmporteerd."

# --- DIT BLOK TOEVOEGEN AAN HET EINDE VAN JE SCRIPT ---
# Schrijf naar GITHUB_OUTPUT in het juiste formaat (key=value)
github_output = os.environ.get('GITHUB_OUTPUT')
if github_output:
    with open(github_output, 'a') as fh:
        fh.write(f"message={bericht}\n")

# Normale prints voor in de GitHub Action log (deze crashen niet)
print(f"Status: 200")
print(f"Log: {bericht}")
