# IDIP — India Disaster Intelligence Platform
## Final Phase Progress Tracker

> **Tagline:** Predict. Prepare. Protect.
> **Solo Project:** Ayush Jain
> **Mode:** ASAP — no fixed deadline
> **Last Updated:** August 17, 2026

---

## Project Reset

All previous episodes (EP1, EP2, EP3, EP4) have been **deleted**.
Jumping directly to **Final Phase** — clean slate, solo sprint.

---

## Final Phase — 7 Stages Overview

| # | Stage | Status |
|---|-------|--------|
| 1 | Data Sources | ✅ Finalized |
| 2 | Data Fetching | 🔄 In Progress |
| 3 | Data Preprocessing | ⏳ Pending |
| 4 | Model Decide | ⏳ Pending |
| 5 | Model Fitting | ⏳ Pending |
| 6 | Model Testing | ⏳ Pending |
| 7 | Deployment | ⏳ Pending |

---

## Stage 1 — Data Sources ✅

### Finalized Source Tier Table

| Tier | Source | Purpose | Access | Status |
|------|--------|---------|--------|--------|
| 0 | **NASA GDIS** | Historical training backbone — 9,924 disasters, 1960–2018, lat/lon included | Manual download — Earthdata login required | ✅ Ready |
| 1 | **USGS** | Earthquakes — magnitude, depth, lat/lon, 1973–present | Free REST API — no key needed | ✅ Ready |
| 1 | **GDACS** | Live events — floods, cyclones, volcanoes, earthquakes, wildfires, droughts | Free API — `pip install gdacs-api` | ✅ Ready |
| 1 | **Open-Meteo** | Weather data — heatwave, precipitation, wind (IMD replacement) | Free — no key, no signup, 10,000 calls/day | ✅ Ready |
| 2 | **ReliefWeb** | Humanitarian reports — validation, impact descriptions | Free REST API — no key needed | ✅ Ready |
| 3 | **NASA FIRMS** | Fire/heat hotspots — MODIS satellite data | Free — MAP_KEY obtained ✅ | ✅ Ready |
| ❌ | ~~IMD~~ | ~~India district-level warnings~~ | ❌ Closed for normal users — IP whitelist only | Replaced by Open-Meteo |

### Data Strategy Decisions
- **File format:** CSV if size is manageable → Parquet if large
- **Coordinates:** lat/lon mandatory in master file
- **State + District:** Will be derived via reverse geocoding from coordinates
- **Scope:** India-focused; all disaster types in one master file

---

## Stage 2 — Data Fetching 🔄

### API Endpoints Confirmed

```
USGS     → https://earthquake.usgs.gov/fdsnws/event/1/query
GDACS    → https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH
ReliefWeb→ https://api.reliefweb.int/v1/disasters
FIRMS    → https://firms.modaps.eosdis.nasa.gov/api/area/csv/<MAP_KEY>/MODIS_NRT/...
Open-Meteo → https://archive-api.open-meteo.com/v1/archive
NASA GDIS  → Manual CSV download from sedac.ciesin.columbia.edu
```

### India Bounding Box (used for filtering)
```
minlat: 6.4   maxlat: 35.5
minlon: 68.7  maxlon: 97.4
```

### Master Schema (Proposed)
```
event_id        → unique ID (source prefix + original ID)
disaster_type   → UPPERCASE standard (EARTHQUAKE, FLOOD, CYCLONE, FIRE, HEATWAVE, DROUGHT...)
date            → YYYY-MM-DD
latitude        → float
longitude       → float
magnitude       → float (intensity/severity normalized)
alert_level     → GREEN / ORANGE / RED / NULL
country         → ISO3 code
state_name      → derived via reverse geocoding
district_name   → derived via reverse geocoding
source          → GDIS / USGS / GDACS / FIRMS / RELIEFWEB / OPEN-METEO
description     → event title/summary
```

### Smoke Test Runner — Built ✅
- File: `src/smoke_runner.py`
- Runs all sources sequentially, tiny sample only (10 records / 1-week window)
- Saves raw responses to `data/raw/<source>/samples/`
- Generates `reports/api_field_inventory.md`
- Detects: pagination, rate limits, auth failures, missing coordinates, date formats
- Commands:
  ```bash
  python src/smoke_runner.py              # all sources
  python src/smoke_runner.py -s usgs     # single source
  ```

### Per-Source Raw Fields Discovered

**USGS:**
```
id, magnitude, place, time (epoch ms), updated, latitude, longitude,
depth_km, magType, type, status, tsunami, sig, alert
```

**GDACS:**
```
event_type (EQ/TC/FL/VO/WF/DR), alert_level (Green/Orange/Red),
country, severity, latitude, longitude, event_name, date, description
```

**ReliefWeb:**
```
name, date, type, country, primary_country, status, glide
⚠️ No direct lat/lon — country level only
```

**NASA GDIS (CSV):**
```
disasterno, year, disastertype, country, iso3, latitude, longitude,
level (admin level 1/2/3)
```

**FIRMS:**
```
latitude, longitude, brightness, scan, track, acq_date, acq_time,
satellite, instrument, confidence, bright_t31, frp, daynight
```

**Open-Meteo:**
```
latitude, longitude, time, temperature_2m_max, precipitation_sum,
wind_speed_10m_max, timezone
```

### Known Issues / Blockers
- ⚠️ **GDACS renamed** — Now "Global Disaster Awareness and Coordination System" (Nov 2025) — API endpoints same, working fine
- ⚠️ **ReliefWeb** — No lat/lon, country-level only → use for validation/description only, not coordinates
- ⚠️ **NASA GDIS** — Manual download only, smoke test only verifies Earthdata credentials
- ❌ **IMD** — Closed for normal users, replaced by Open-Meteo
- ℹ️ **FIRMS MAP_KEY** — Obtained, stored in `.env` only (never hardcode!)

---

## Stage 3 — Data Preprocessing ⏳

**Not started yet.**

Planned steps:
- [ ] Load all raw source files
- [ ] Normalize disaster_type naming across sources
- [ ] Standardize date format → `YYYY-MM-DD`
- [ ] Normalize coordinates to float
- [ ] Reverse geocoding: lat/lon → state_name + district_name
- [ ] Merge all into one master file
- [ ] Handle missing values, duplicates, outliers
- [ ] Save as CSV (small) or Parquet (large)

---

## Stage 4 — Model Decide ⏳

**Not started. To be discussed.**

---

## Stage 5 — Model Fitting ⏳

**Not started.**

---

## Stage 6 — Model Testing ⏳

**Not started.**

Planned metrics (TBD):
- Precision, Recall
- MAE, RMSE (if regression)
- Accuracy / F1 (if classification)

---

## Stage 7 — Deployment ⏳

**Not started.**

### Prototype App Plan
- **Framework:** Streamlit (simple, fast)
- **Must show:**
  - Coordinates (lat/lon)
  - state_name
  - district_name
  - Disaster type, date, severity
- **Preferred:** Interactive map (Folium or Plotly)

---

## Tech Stack (Decided So Far)

```
Language      → Python
Data format   → CSV / Parquet
Reverse geo   → TBD (geopy / Nominatim / Google Maps)
Dashboard     → Streamlit
Map           → Folium or Plotly
Env mgmt      → python-dotenv (.env file)
HTTP client   → requests (with retry + backoff)
```

---

## Key Files Built

| File | Purpose |
|------|---------|
| `src/smoke_runner.py` | Unified API smoke test runner |
| `.env.example` | Environment variable template |
| `.gitignore` | Keeps `.env` out of git |
| `requirements.txt` | `requests`, `python-dotenv` |
| `README.md` | Full setup + run instructions |

---

## Quick Reference — Run Commands

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env   # fill in keys

# Smoke test — all sources
python src/smoke_runner.py

# Smoke test — single source
python src/smoke_runner.py -s usgs
python src/smoke_runner.py -s gdacs
python src/smoke_runner.py -s firms
python src/smoke_runner.py -s reliefweb
python src/smoke_runner.py -s gdis
```

---

## Next Immediate Step

> **Fix smoke runner error → confirm all APIs returning data → move to Stage 3 (Preprocessing)**
