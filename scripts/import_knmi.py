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

# KNMI stations (kan later uitgebreid worden)
stations = [
    260,  # De Bilt
    370,  # Eindhoven
    235,  # De Kooy
    240,  # Schiphol
    344   # Rotterdam
]

for station in stations:

    print(f"Download station {station}")

    url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"

    response = requests.post(
        url,
        data={
            "stns": station,
            "vars": "TX,TN,RH"
        }
    )

    df = pd.read_csv(
        StringIO(response.text),
        comment="#",
        sep=","
    )

    df["station"] = station

    df.rename(
        columns={
            "YYYYMMDD": "datum",
            "TX": "temp_max",
            "TN": "temp_min",
            "RH": "regen"
        },
        inplace=True
    )

    df["temp_max"] = df["temp_max"] / 10
    df["temp_min"] = df["temp_min"] / 10
    df["regen"] = df["regen"] / 10

    df[
        [
            "datum",
            "station",
            "temp_max",
            "temp_min",
            "regen"
        ]
    ].to_sql(
        "measurements",
        conn,
        if_exists="append",
        index=False
    )


conn.commit()
conn.close()

print("KNMI import klaar")
