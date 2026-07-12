import sqlite3
import pandas as pd
import requests
from io import StringIO
import os

os.makedirs("database", exist_ok=True)

DB = "database/knmi_weather.db"

conn = sqlite3.connect(DB)

conn.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    datum TEXT,
    station INTEGER,
    temp_max REAL,
    temp_min REAL,
    regen REAL
)
""")

# KNMI daggegevens open data
url = "https://cdn.knmi.nl/knmi/map/page/klimatologie/gegevens/daggegevens/daggegevens.zip"

print("Download KNMI bestand")

response = requests.get(url)

if response.status_code != 200:
    print("Download mislukt:", response.status_code)
    exit()

with open("daggegevens.zip", "wb") as f:
    f.write(response.content)

print("Bestand binnen")


import zipfile

with zipfile.ZipFile("daggegevens.zip") as z:
    z.extractall("knmi_data")


bestanden = os.listdir("knmi_data")

print(bestanden)


for bestand in bestanden:

    if bestand.endswith(".txt"):

        pad = "knmi_data/" + bestand

        print("Lees:", pad)

        df = pd.read_csv(
            pad,
            comment="#",
            sep=",",
            skipinitialspace=True
        )

        print(df.head())

        break


print("KNMI import klaar")
