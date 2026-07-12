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
        WHERE substr(REPLACE(datum,'-',''),5,2)=?
        AND substr(REPLACE(datum,'-',''),7,2)=?
        ORDER BY {kolom} {volgorde}
        LIMIT 1
    """, (maand, dag))

    return cursor.fetchone()


def maak_record(record):
    if record:
        return {
            "datum": record[0],
            "station": record[1],
            "waarde": record[2]
        }

    return {
        "datum": "geen data",
        "station": "onbekend",
        "waarde": None
    }


records = {
    "datum": f"{dag}-{maand}",
    "warmste": maak_record(zoek_record("temp_max", "DESC")),
    "koudste": maak_record(zoek_record("temp_min", "ASC")),
    "natste": maak_record(zoek_record("regen", "DESC"))
}


conn.close()


with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("Dagrecords gemaakt")
