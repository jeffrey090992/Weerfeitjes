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

stations = [
    260,
    370,
    235,
    240,
    344
]

url = "https://www.daggegevens.knmi.nl/klimatologie/daggegevens"


for station in stations:

    print(f"Download station {station}")

    response = requests.post(
        url,
        data={
            "stns": str(station),
            "vars": "TX,TN,RH",
            "start": "19010101",
            "end": "20251231"
        },
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    if response.status_code != 200:
        print("KNMI fout:", response.status_code)
        continue

    if "<html" in response.text.lower():
        print("Geen CSV ontvangen")
        continue


    df = pd.read_csv(
        StringIO(response.text),
        comment="#",
        sep=","
    )


    print(df.head())


    if "STN" in df.columns:
        df.drop(columns=["STN"], inplace=True)


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


    df = df[
        [
            "datum",
            "station",
            "temp_max",
            "temp_min",
            "regen"
        ]
    ]


    df["temp_max"] = pd.to_numeric(df["temp_max"], errors="coerce") / 10
    df["temp_min"] = pd.to_numeric(df["temp_min"], errors="coerce") / 10
    df["regen"] = pd.to_numeric(df["regen"], errors="coerce") / 10


    df.dropna(inplace=True)


    print("Aantal regels:", len(df))


    df.to_sql(
        "measurements",
        conn,
        if_exists="append",
        index=False
    )


cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM measurements")
print("Totaal:", cursor.fetchone()[0])


conn.commit()
conn.close()

print("KNMI import klaar")
