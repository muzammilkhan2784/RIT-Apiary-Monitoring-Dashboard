import os
import csv
from datetime import datetime
from pymongo import MongoClient

# === MongoDB Setup ===
client = MongoClient("mongodb://localhost:27017/")
db     = client["apiary"]
collection = db["hive_readings"]

# === BroodMinder map ===
device_map = {
    "56_40_52": ("C", "broodminder"),
    "56_40_58": ("B", "broodminder"),
    "56_40_59": ("E", "broodminder"),
    "63_06_7C": ("E", "broodminder"),
    "63_06_7D": ("B", "broodminder")
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BROODMINDER_FOLDER = os.path.join(BASE_DIR, "2025-04-22")
DIY_FOLDER          = BASE_DIR

def safe_float(val):
    try:
        v = val.strip().lower()
        if v in ("","undefined","null","nan","false"):
            return None
        return float(val)
    except:
        return None

def import_broodminder():
    print("\n--- Importing BroodMinder data ---")
    for fn in os.listdir(BROODMINDER_FOLDER):
        if not fn.endswith(".csv"):
            continue
        code = fn.split("_hist")[0].replace("-", "_")
        hive, src = device_map.get(code, ("?", "broodminder"))
        path = os.path.join(BROODMINDER_FOLDER, fn)
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts_raw = row.get("UTC_TimeStamp","").strip()
                ts = None
                for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ","%m/%d/%Y %I:%M:%S %p","%m/%d/%Y %I:%M %p"):
                    try:
                        ts = datetime.strptime(ts_raw, fmt)
                        break
                    except:
                        pass
                if not ts:
                    # skip bad timestamp
                    continue
                meas = {}
                for key in ["Temperature","Humidity","Battery","ChargeRemaining","Radar1","Radar2","Audio1","Audio2"]:
                    if key in row:
                        fv = safe_float(row[key])
                        if fv is not None:
                            meas[key.lower()] = fv
                if not meas:
                    continue
                doc = {
                    "hive": hive,
                    "source": src,
                    "device_id": code,
                    "timestamp": ts,
                    "measurements": meas
                }
                collection.insert_one(doc)
    print("✓ BroodMinder import complete.")

def import_diy():
    print("\n--- Importing DIY data ---")
    file_map = {"hive b.txt":"B","hive c.txt":"C","hive e.txt":"E"}
    for fn, hive in file_map.items():
        path = os.path.join(DIY_FOLDER, fn)
        if not os.path.exists(path):
            continue
        with open(path) as f:
            for line in f:
                parts = [p.strip() for p in line.split("|")]
                if parts[0].lower()=="monitor id" or len(parts)!=8:
                    continue
                mid, ts, ht, hh, ha, et, ep, bl = parts
                try:
                    timestamp = datetime.fromisoformat(ts)
                except:
                    continue
                meas = {
                    "hive_temp": safe_float(ht),
                    "hive_humidity": safe_float(hh),
                    "hive_acoustics": safe_float(ha),
                    "external_temp": safe_float(et),
                    "external_pressure": safe_float(ep),
                    "battery_life": safe_float(bl)
                }
                if all(v is None for v in meas.values()):
                    continue
                doc = {
                    "hive": hive,
                    "source": "diy",
                    "device_id": mid,
                    "timestamp": timestamp,
                    "measurements": meas
                }
                collection.insert_one(doc)
    print("✓ DIY import complete.")

if __name__ == "__main__":
    import_broodminder()
    import_diy()
    print("\n All data imported successfully!")
