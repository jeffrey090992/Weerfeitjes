import sqlite3
import json
import os

DB = "database/knmi_weather.db"
OUTPUT = "records.json"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

# Warmste dag
cursor.execute("""
SELECT datum, station, temp_max
FROM measurements
ORDER BY temp_max DESC
LIMIT 1
""")
warmste = cursor.fetchone()

# Koudste dag
cursor.execute("""
SELECT datum, station, temp_min
FROM measurements
ORDER BY temp_min ASC
LIMIT 1
""")
koudste = cursor.fetchone()

# Meeste regen
cursor.execute("""
SELECT datum, station, regen
FROM measurements
ORDER BY regen DESC
LIMIT 1
""")
natste = cursor.fetchone()

conn.close()

records = {
    "warmste_dag": {
        "datum": warmste[0],
        "station": warmste[1],
        "temperatuur": warmste[2]
    },
    "koudste_dag": {
        "datum": koudste[0],
        "station": koudste[1],
        "temperatuur": koudste[2]
    },
    "natste_dag": {
        "datum": natste[0],
        "station": natste[1],
        "regen_mm": natste[2]
    }
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("Records opgeslagen:", OUTPUT)
