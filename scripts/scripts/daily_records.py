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

# Warmste dagrecord
cursor.execute("""
SELECT datum, station, temp_max
FROM measurements
WHERE substr(datum,5,2)=?
AND substr(datum,7,2)=?
ORDER BY temp_max DESC
LIMIT 1
""", (maand, dag))

warmste = cursor.fetchone()


# Koudste dagrecord
cursor.execute("""
SELECT datum, station, temp_min
FROM measurements
WHERE substr(datum,5,2)=?
AND substr(datum,7,2)=?
ORDER BY temp_min ASC
LIMIT 1
""", (maand, dag))

koudste = cursor.fetchone()


# Natste dagrecord
cursor.execute("""
SELECT datum, station, regen
FROM measurements
WHERE substr(datum,5,2)=?
AND substr(datum,7,2)=?
ORDER BY regen DESC
LIMIT 1
""", (maand, dag))

natste = cursor.fetchone()

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
