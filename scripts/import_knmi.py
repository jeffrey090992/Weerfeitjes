import sqlite3
import requests
import pandas as pd
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

# KNMI stations
stations = [
    260,  # De Bilt
    370,  # Eindhoven
    235,  # De Kooy
    240,  # Schiphol
    344   # Rotterdam
]

url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"


for station in stations:

    print(f"Download station {station}")

    response = requests.post(
        url,
        data={
            "stns": station,
            "vars": "TX,TN,RH",
            "start": "19010101",
            "end": "20251231"
        }
    )

    print(response.text[:300])

    if response.status_code != 200:
        print(f"Fout bij station {station}")
        continue


    try:
        df = pd.read_csv(
            StringIO(response.text),
            comment="#",
            sep=",",
            skipinitialspace=True
        )

    except Exception as e:
        print("Fout bij inlezen:")
        print(e)
        continue


    print(df.head())
    print(df.columns)


    # Station verwijderen als KNMI hem meestuurt
    if "STN" in df.columns:
        df.drop(columns=["STN"], inplace=True)


    df["station"] = station


    # Kolommen hernoemen
    df.rename(
        columns={
            "YYYYMMDD": "datum",
            "TX": "temp_max",
            "TN": "temp_min",
            "RH": "regen"
        },
        inplace=True
    )


    # Alleen benodigde kolommen
    df = df[
        [
            "datum",
            "station",
            "temp_max",
            "temp_min",
            "regen"
        ]
    ]


    # KNMI waarden omzetten
    df["temp_max"] = pd.to_numeric(
        df["temp_max"],
        errors="coerce"
    ) / 10

    df["temp_min"] = pd.to_numeric(
        df["temp_min"],
        errors="coerce"
    ) / 10

    df["regen"] = pd.to_numeric(
        df["regen"],
        errors="coerce"
    ) / 10


    # Lege regels verwijderen
    df.dropna(inplace=True)


    print(f"{len(df)} metingen gevonden")


    # Opslaan
    df.to_sql(
        "measurements",
        conn,
        if_exists="append",
        index=False
    )


    print(f"Station {station} klaar")


# Controle
cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM measurements"
)

aantal = cursor.fetchone()[0]

print("Totaal aantal metingen:", aantal)


conn.commit()
conn.close()

print("KNMI import klaar")
