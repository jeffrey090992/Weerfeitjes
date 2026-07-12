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
        WHERE substr(datum,5,2)=?
        AND substr(datum,7,2)=?
        ORDER BY {kolom} {volgorde}
        LIMIT 1
    """, (maand, dag))

    return cursor.fetchone()


warmste = zoek_record("temp_max", "DESC")
koudste = zoek_record("temp_min", "ASC")
natste = zoek_record("regen", "DESC")


conn.close()


records = {
    "datum": f"{dag}-{maand}",

    "warmste": {
        "datum": warmste[0],
        "station": warmste[1],
        "waarde": warmste[2]
    },

    "koudste": {
        "datum": koudste[0],
        "station": koudste[1],
        "waarde": koudste[2]
    },

    "natste": {
        "datum": natste[0],
        "station": natste[1],
        "waarde": natste[2]
    }
}


with open(OUTPUT, "w", encoding="utf-8") as bestand:
    json.dump(records, bestand, indent=4, ensure_ascii=False)


print("Dagrecords gemaakt")
