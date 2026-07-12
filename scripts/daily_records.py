import sqlite3
import json
from datetime import datetime

DB = "database/knmi_weather.db"
OUTPUT = "daily_records.json"

vandaag = datetime.now()

dag = f"{vandaag.day:02d}"
maand = f"{vandaag.month:02d}"

conn = sqlite3.connect(DB)
cursor = conn.cursor()


def zoek_record(kolom, volgorde):
    cursor.execute(f"""
        SELECT datum, station, {kolom}
        FROM measurements
        WHERE substr(CAST(datum AS TEXT), 5, 2) = ?
        AND substr(CAST(datum AS TEXT), 7, 2) = ?
        ORDER BY {kolom} {volgorde}
        LIMIT 1
    """, (maand, dag))

    return cursor.fetchone()


warmste = zoek_record("temp_max", "DESC")
koudste = zoek_record("temp_min", "ASC")
natste = zoek_record("regen", "DESC")

conn.close()


def maak_record(data):
    if data:
        return {
            "datum": data[0],
            "station": data[1],
            "waarde": data[2]
        }
    else:
        return {
            "datum": "geen data",
            "station": "onbekend",
            "waarde": None
        }


records = {
    "datum": f"{dag}-{maand}",
    "warmste": maak_record(warmste),
    "koudste": maak_record(koudste),
    "natste": maak_record(natste)
}


with open(OUTPUT, "w", encoding="utf-8") as bestand:
    json.dump(records, bestand, indent=4, ensure_ascii=False)


print("Dagrecords gemaakt")
