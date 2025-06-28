# 🐝 ISTE-438 Bonus Project: RIT Apiary Data Dashboard

## Summary of Work Completed

For the bonus project, I built a complete interactive data dashboard to visualize RIT Apiary sensor data using MongoDB, Flask, and Chart.js. The app integrates **BroodMinder** and **DIY sensors** across Hives B, C, and E, offering time-based insight into hive conditions such as temperature, humidity, and acoustics.

###  Features Implemented

- **MongoDB Time-Series Collection**
  - Created `hive_readings` with `timestamp` as `timeField` and `hive` as `metaField`.
  - Enables efficient time-based querying and aggregation.

- **Data Import**
  - Parsed and imported all **BroodMinder CSVs** (temperature, humidity, battery, radar, audio).
  - Parsed **DIY sensor logs** (hive temperature, acoustics, external pressure, etc.).
  - Used custom `import.py` script for cleaning and formatting.

- **Interactive Flask App**
  - User can:
    - Choose Hive (B, C, E) and Source (BroodMinder, DIY, or Both).
    - Select individual sensors to graph.
    - Filter by date range (via date picker).
    - Toggle **Moving Average** smoothing.
    - Toggle **Colony Event Detection** overlay.

- **Colony Event Detection**
  - Detects:
    - **Brood-rearing** → sharp temp rise (≥ +2.5°C).
    - **Die-offs** → sharp drop (≤ -3°C).
  - Annotated on the chart with:
    - Green lines for brood-rearing.
    - Red lines for die-offs.

- **User-Friendly Summary**
  - After plotting, an auto-generated summary appears:
    - "From Oct 1 to Oct 31, Hive B’s temperature rose 6 times and dropped 4 times..."
  - Language is readable for non-experts (no jargon).
  
- **Polished UI**
  - Aesthetic improvements:
    - Modern layout, spacing, and font use.
    - Styled dropdowns, checkboxes, and button.
    - Responsive layout.
    - Clearly grouped sensors by source (BroodMinder vs DIY).
    - Friendly date format: `Nov 12, 2024`.

---

## Screenshots

You should include these screenshots when submitting:

1. **Chart** with hive temperature, moving average, and brood/die-off markers.
2. **Multi-sensor chart** comparing variables like humidity and battery.
3. **Event summary** paragraph.
4. **Full form UI** showing hive/source/sensor/date selection.

---

## Bonus Points Expected: **3**

I believe this project meets the full 3-point bonus criteria because:

- ✅ Designed a MongoDB time-series model.
- ✅ Imported both BroodMinder and DIY datasets.
- ✅ Built an interactive Flask + Chart.js visualization dashboard.
- ✅ Added advanced features:
  - Automatic colony event detection.
  - Moving average overlay.
  - Clean UI with responsive layout.


---

### Thank you!
