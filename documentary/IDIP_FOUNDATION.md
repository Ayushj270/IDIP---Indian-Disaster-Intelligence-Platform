# IDIP — Project Foundation

## 1. Product goal

IDIP is an India-focused disaster intelligence and risk platform.

A user enters a coordinate, state, or district. The product resolves that input to a location and shows:

- current disaster events and official warnings near that place;
- current environmental conditions such as rainfall, temperature, soil moisture, and active fires;
- predicted risk for the next 6, 24, and 72 hours where a scientifically valid model is available;
- a map, evidence behind the risk, source freshness, and confidence.

The product must clearly distinguish **observed events**, **official warnings**, and **modelled risk**.

> IDIP must not claim to predict the exact time or location of earthquakes or volcanic eruptions. Those modules show authoritative alerts, event history, and exposure context.

## 2. Priority hazards

The main hazards are:

1. Earthquake
2. Flood
3. Cyclone
4. Wildfire
5. Landslide
6. Volcano
7. Heatwave
8. Heavy rainfall

## 3. Data strategy

NASA Earthdata remains a key source for historical and environmental observations, but the platform should not rely on manually downloading and inspecting unrelated files.

Use two data layers:

| Layer | Purpose | Examples |
|---|---|---|
| Event and warning layer | What is happening or has happened | GDACS, USGS, FIRMS, IMD, GDIS, ReliefWeb |
| Environmental feature layer | Conditions used to assess or model risk | GPM IMERG, MERRA-2, SMAP, NASADEM, satellite imagery |

The user interface reads from the IDIP database. It must not make calls to every upstream provider whenever a user searches.

## 4. Core sources and current access status

| Source | Role | Current decision |
|---|---|---|
| [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/) | Live and historical earthquake events | Use now; public and no API key required |
| [GDACS API](https://www.gdacs.org/gdacsapi/swagger/index.html) | Global active events and alerts: earthquakes, cyclones, floods, volcanoes, wildfires, droughts | Use after correcting query parameters and pagination |
| [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/api/area/) | Near-real-time active-fire detections | Use after obtaining a free `MAP_KEY` |
| [ReliefWeb API](https://apidoc.reliefweb.int/) | Disaster metadata, reports, humanitarian context | Use API v2 with an approved `appname`; do not use the obsolete v1 URL |
| [IMD API reference](https://api.imd.gov.in/public/api_reference.html) | India weather, district warnings, nowcasts, rainfall, cyclone information | Access is protected; confirm API-key and/or IP approval requirements before making it a core dependency |
| [NASA GDIS](https://catalog.data.gov/dataset/geocoded-disasters-gdis-dataset-bd107) | Historical, geocoded disaster locations and impacts | One-time, versioned historical import; not a live API |
| [NASA EONET](https://eonet.gsfc.nasa.gov/docs/v3) | Near-real-time natural-event metadata and related layers | Optional supporting event feed |
| [Open-Meteo](https://open-meteo.com/en/docs) | Coordinate-based forecast features for a prototype | Optional forecast input; never present it as an official India warning |

### Initial live-source set

Start with **USGS + GDACS + FIRMS**. Add ReliefWeb after its v2 configuration is confirmed. Temporarily exclude IMD until official access is established. Import GDIS separately as historical training data.

## 5. NASA environmental data for modelling

Do not download every NASA collection. Begin only with the datasets that support the first weather-driven risk models.

| Dataset | Use |
|---|---|
| GPM IMERG | Rainfall, heavy-rainfall, flood, cyclone, and landslide features |
| MERRA-2 | Temperature, humidity, wind, and heatwave features |
| SMAP | Soil-moisture features for flood and landslide risk |
| NASADEM | Elevation and slope features for flood and landslide risk |
| FIRMS | Current fire detections; later wildfire-risk features |

Use the `earthaccess` / NASA CMR workflow to search, stream, or download only the required area, time range, and variables. Keep raw NASA files unchanged.

## 6. Data architecture

```text
Provider API or historical file
            ↓
Raw storage (unchanged response)
            ↓
Source-specific adapter and validation
            ↓
Canonical IDIP event and observation tables
            ↓
Feature tables and risk models
            ↓
Location dashboard and API
```

### Storage layout

```text
data/raw/          untouched source responses and imported source files
data/normalized/   source data converted to IDIP conventions
data/features/     location-and-date model features
reports/           API schema inventories and ingestion reports
logs/              ingestion logs
```

Recommended storage technologies:

- **PostgreSQL + PostGIS** for current events, geometry, locations, districts, warnings, and user-location queries.
- **Parquet** for large historical event, observation, and feature datasets.
- Object/file storage for untouched raw source payloads.

Do not commit `data/`, `logs/`, `.env`, downloaded files, or API keys to Git.

## 7. Canonical IDIP event schema

Every incoming record is stored in its original form and transformed into a normalized record where possible.

```text
source
source_event_id
hazard_type
event_name
status
start_time_utc
end_time_utc
time_precision
latitude
longitude
geometry
spatial_precision
country_iso3
admin_level
source_alert_level
idip_risk_level
source_url
fetched_at
raw_payload
```

### Event metrics table

Do not create hundreds of hazard-specific columns in the main event table. Store measurements separately:

```text
event_id | metric_name | metric_value | metric_unit
```

Examples:

```text
USGS_001 | magnitude        | 6.2  | Mw
USGS_001 | depth            | 12   | km
GDACS_88 | wind_speed       | 120  | km/h
GDACS_88 | affected_people  | 5000 | persons
```

### Universal normalization rules

- Store all timestamps in UTC.
- Use WGS84 / EPSG:4326 for latitude, longitude, and geometry.
- Convert values to a documented common unit when appropriate, while retaining the source value and unit.
- Map source hazard names and codes to a fixed IDIP hazard taxonomy.
- Use `null` for missing values; never replace missing data with `0`.
- Preserve `source_alert_level` exactly as supplied.
- Calculate `idip_risk_level` separately; source severity scales are not directly comparable.
- Never invent precision: GDIS `year` remains `event_year` with `time_precision = year`.
- A country-only report has `spatial_precision = country`; do not fabricate point coordinates.

## 8. Source mapping rules

| Source | Identifier | Location | Time | Important handling |
|---|---|---|---|---|
| GDIS | `disasterno` | `latitude`, `longitude` | `year` only | Preserve year precision and `level` admin level |
| USGS | `id` | GeoJSON point: `[longitude, latitude, depth]` | Epoch milliseconds | Map type to `earthquake`; store magnitude and depth as metrics |
| GDACS | Event type + event ID + episode ID when available | Preserve supplied GeoJSON geometry | ISO dates | Use documented codes such as `EQ`, `TC`, `FL`, `VO`, `WF`, `DR`; preserve Green/Orange/Red source alert |
| ReliefWeb | ReliefWeb ID | Usually country-level, not a guaranteed point | ISO dates | Store as contextual report data, not as a precise event point |
| FIRMS | Stable source observation identifier or composite key | Latitude/longitude fire point | Acquisition date and time | Preserve sensor, confidence, FRP, and source-product fields |
| IMD | Official warning / station / district ID | Depends on endpoint | Endpoint-specific | Preserve official category and colour code |

## 9. API adapter requirements

Each provider receives its own adapter. Adapters transform a copy of raw data; they never overwrite raw payloads.

Every adapter must:

1. Read keys only from environment variables.
2. Use a small smoke-test sample before any historical fetch.
3. Apply timeouts, retries, rate-limit backoff, and pagination.
4. Save the untouched response.
5. Validate required fields, data types, coordinate ranges, and time formats.
6. Quarantine malformed records instead of silently discarding them.
7. Emit a field inventory across **all sampled records**, not only the first response record.
8. Redact secrets from URLs, logs, reports, and error messages.

## 10. Smoke-test runner review

The generated runner at `idip_smoke_test_1/idip_smoke_test/src/smoke_runner.py` is a useful initial skeleton. It has the correct goals: small source samples, raw-response preservation, source selection, logs, and a field-inventory report.

It must be corrected before the full suite is run:

- Treat all non-2xx HTTP responses as failures; otherwise a 404/500 can be marked as passed.
- Use GDACS `eventlist` parameters (for example `EQ;TC;FL`) and preserve full geometry rather than assuming a point coordinate pair.
- Move ReliefWeb from the retired v1 endpoint to v2.
- Redact the FIRMS `MAP_KEY`; the current full endpoint would expose it in reports.
- Use IMD `/api/v1/districtwarning` after access approval, not `/warnings/district`.
- Do not validate GDIS credentials with a landing-page `HEAD` request; test a real protected asset or import the static dataset once.
- Build field inventory from the union of keys across all sampled records.
- Use a real CSV parser such as Python `csv.DictReader` for FIRMS responses.

Run sources one at a time after these fixes:

```text
python src/smoke_runner.py --source usgs
python src/smoke_runner.py --source gdacs
python src/smoke_runner.py --source firms
```

## 11. Model plan

IDIP should use multiple focused risk models behind one user experience, not one universal disaster model.

### First predictive scope

Build separate **LightGBM** models for:

1. Heavy rainfall
2. Flood
3. Landslide

These hazards share rainfall, soil moisture, terrain, and weather features and are realistic for the first India-focused model.

### Initial model outputs

For each grid cell or resolved user location:

```text
hazard_type
forecast_horizon_hours
probability
risk_level
confidence
evidence_features
data_freshness
```

Examples of evidence features:

- rainfall in the last 1, 24, 72 hours, and 7 days;
- forecast rainfall, wind, temperature, and humidity;
- soil moisture;
- elevation and slope;
- historical event density;
- nearby observed events and official warnings.

### Hazard-specific product handling

| Hazard | Initial approach |
|---|---|
| Heavy rainfall | LightGBM risk model using rainfall and forecast features |
| Flood | LightGBM risk model using rainfall, soil moisture, terrain, and drainage/exposure features |
| Landslide | LightGBM risk model using cumulative rain, soil moisture, slope, elevation, land cover, and historical labels |
| Heatwave | Threshold-based risk first; model later using MERRA-2 and forecast temperature/humidity |
| Wildfire | FIRMS observed-fire overlay first; risk model later |
| Cyclone | Official track/warning overlay plus rainfall and wind risk; no independent track model in V1 |
| Earthquake | USGS observed-event and hazard/exposure display; no earthquake prediction claim |
| Volcano | Authoritative observed-event display and risk context; no eruption prediction claim |

## 12. Immediate next steps

1. Fix the smoke-test runner issues in Section 10.
2. Collect one real, small sample response from each accessible source.
3. Generate and review `reports/api_field_inventory.md`.
4. Create the final source-field-to-canonical-field mapping document.
5. Implement raw, normalized, and feature storage.
6. Import GDIS as a versioned historical dataset.
7. Start live ingestion with USGS, GDACS, and FIRMS.
8. Build the first heavy-rainfall, flood, and landslide feature table.
9. Train and evaluate the first LightGBM models only after labels and data-quality checks are complete.

