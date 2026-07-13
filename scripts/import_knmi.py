import os

# --- JOUW BESTAANDE LOGICA HIER ---
aantal_records = 5 
bericht = f"Succesvol {aantal_records} dagrecords geïmporteerd."

# --- OUTPUT NAAR GITHUB ---
github_output = os.environ.get('GITHUB_OUTPUT')
if github_output:
    with open(github_output, 'a') as fh:
        fh.write(f"message={bericht}\n")

# Normale prints voor in de GitHub Action log
print(f"Status: 200")
print(f"Log: {bericht}")
