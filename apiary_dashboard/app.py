from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.apiary
collection = db.hive_readings

def detect_events(points):
    raw = []
    for i in range(1, len(points)):
        d0, v0 = points[i-1]
        d1, v1 = points[i]
        delta = v1 - v0
        if delta >= 2.5:
            raw.append((d1, "brood-rearing", round(delta,1)))
        elif delta <= -3:
            raw.append((d1, "die-off", round(-delta,1)))
    daily = {}
    for dt, typ, ch in raw:
        day = dt.date().isoformat()
        if day not in daily or ch > daily[day]["change"]:
            daily[day] = {"date": day, "type": typ, "change": ch}
    return [daily[d] for d in sorted(daily)]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    hive    = request.args.get("hive")
    source  = request.args.get("source")
    sensors = request.args.getlist("sensors")
    start   = request.args.get("start")
    end     = request.args.get("end")

    sd = datetime.strptime(start, "%Y-%m-%d")
    ed = datetime.strptime(end,   "%Y-%m-%d")

    series = []
    all_events = []

    for sensor in sensors:
        q = {
            "hive": hive,
            f"measurements.{sensor}": {"$exists": True},
            "timestamp": {"$gte": sd, "$lte": ed}
        }
        if source in ("broodminder","diy"):
            q["source"] = source

        docs = list(collection.find(q).sort("timestamp",1))
        pts  = [(d["timestamp"], d["measurements"][sensor]) for d in docs]

        series.append({
            "sensor": sensor,
            "points": [{"x": t.isoformat(), "y": v} for t,v in pts]
        })
        all_events.extend(detect_events(pts))

    brood = [e for e in all_events if e["type"]=="brood-rearing"]
    die   = [e for e in all_events if e["type"]=="die-off"]
    summary = {
        "broodCount": len(brood),
        "dieCount":   len(die),
        "largestBrood": max(brood, key=lambda e:e["change"]) if brood else None,
        "largestDie":  max(die,   key=lambda e:e["change"]) if die   else None
    }

    return jsonify(series=series, events=all_events, summary=summary)

if __name__=="__main__":
    app.run(debug=True)
