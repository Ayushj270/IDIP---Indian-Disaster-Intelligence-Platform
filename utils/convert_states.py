# ============================================================
# 29.01 — IMPORT LIBRARIES
# ============================================================

import geopandas as gpd
from pathlib import Path
from shapely.geometry import MultiPolygon

# ============================================================
# 29.02 — PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

SHAPEFILE_DIR = (

    PROJECT_DIR
    / "shapfiles"
)

INPUT_FILE = (

    SHAPEFILE_DIR
    / "india_states.shp"
)

OUTPUT_SHP = (

    SHAPEFILE_DIR
    / "india_states_clean.shp"
)

OUTPUT_GEOJSON = (
    SHAPEFILE_DIR
    / "india_states.geojson"
)

# ============================================================
# 29.03 — LOAD ORIGINAL SHAPEFILE
# ============================================================

print("\nLoading original shapefile...")
shp = gpd.read_file(INPUT_FILE)
print("Shapefile loaded successfully.\n")
print("Original total features:")
print(len(shp))
print("\nAvailable columns:")
print(list(shp.columns))
print("\nCurrent CRS:")
print(shp.crs)

# ============================================================
# 29.04 — ENSURE CORRECT CRS
# ============================================================

if shp.crs is None:

    print("\nWARNING: No CRS found.")
    print("Assigning EPSG:4326...")

    shp = shp.set_crs(
        "EPSG:4326"
    )

else:

    print("\nConverting CRS to EPSG:4326...")

    shp = shp.to_crs(
        "EPSG:4326"
    )

# ============================================================
# 29.05 — REMOVE UNNECESSARY COLUMNS
# ============================================================

columns_to_remove = [

    "fid",
    "cat"
]

for column in columns_to_remove:

    if column in shp.columns:

        shp = shp.drop(
            columns=column
        )

# ============================================================
# 29.06 — CHECK REQUIRED STATE COLUMN
# ============================================================

if "ST_NM" not in shp.columns:

    raise ValueError(

        "\nERROR: 'ST_NM' column was not found.\n"
        f"Available columns: {list(shp.columns)}"
    )

# ============================================================
# 29.07 — STATE NAME TO STATE ID MAPPING
# ============================================================

ST_ID = {

    "Andhra Pradesh": "IN-AP",
    "Arunachal Pradesh": "IN-AR",
    "Assam": "IN-AS",
    "Bihar": "IN-BR",
    "Chhattisgarh": "IN-CT",
    "Goa": "IN-GA",
    "Gujarat": "IN-GJ",
    "Haryana": "IN-HR",
    "Himachal Pradesh": "IN-HP",
    "Jharkhand": "IN-JH",
    "Karnataka": "IN-KA",
    "Kerala": "IN-KL",
    "Madhya Pradesh": "IN-MP",
    "Maharashtra": "IN-MH",
    "Manipur": "IN-MN",
    "Meghalaya": "IN-ML",
    "Mizoram": "IN-MZ",
    "Nagaland": "IN-NL",
    "Odisha": "IN-OR",
    "Punjab": "IN-PB",
    "Rajasthan": "IN-RJ",
    "Sikkim": "IN-SK",
    "Tamil Nadu": "IN-TN",
    "Telangana": "IN-TG",
    "Tripura": "IN-TR",
    "Uttar Pradesh": "IN-UP",
    "Uttarakhand": "IN-UT",
    "West Bengal": "IN-WB",
    "Andaman & Nicobar Island": "IN-AN",
    "Andaman and Nicobar Islands": "IN-AN",
    "Chandigarh": "IN-CH",
    "Dadara & Nagar Havelli": "IN-DN",
    "Dadra & Nagar Haveli": "IN-DN",
    "Dadra and Nagar Haveli": "IN-DN",
    "Daman & Diu": "IN-DD",
    "Daman and Diu": "IN-DD",
    "Delhi": "IN-DL",
    "NCT of Delhi": "IN-DL",
    "Jammu & Kashmir": "IN-JK",
    "Jammu and Kashmir": "IN-JK",
    "Ladakh": "IN-LA",
    "Lakshadweep": "IN-LD",
    "Puducherry": "IN-PY"
}

# ============================================================
# 29.08 — VERIFY ALL STATE NAMES
# ============================================================

unique_states = sorted(
    shp["ST_NM"]
    .dropna()
    .unique()
)

missing_states = [
    state
    for state in unique_states
    if state not in ST_ID
]

if missing_states:
    print(
        "\nWARNING!"
    )

    print(
        "These state names are not present "
        "in the ST_ID dictionary:\n"
    )

    for state in missing_states:
        print(
            f"- {state}"
        )

    raise ValueError(
        "\nPlease add the missing state names "
        "before converting."
    )

print(
    "\nAll state names verified successfully."
)

# ============================================================
# 29.09 — CREATE STATE ID COLUMNS
# ============================================================

shp["ST_ID"] = (
    shp["ST_NM"]
    .map(ST_ID)
)

shp["ID"] = (
    shp["ST_ID"]
    .str.replace(
        "IN-",
        "",
        regex=False
    )
)

# ============================================================
# 29.10 — DISSOLVE GEOMETRIES BY STATE
# ============================================================

print(
    "\nDissolving state geometries..."
)

india_states = (

    shp.dissolve(
        by="ST_NM",
        as_index=False,
        aggfunc="first"
    )
)

print(

    "State geometries dissolved successfully."
)

# ============================================================
# 29.10.01 — CLEAN JAMMU & KASHMIR GEOMETRY
# ============================================================

print(
    "\nCleaning Jammu & Kashmir geometry..."
)

jk_mask = (

    india_states["ST_NM"]
    .isin([
        "Jammu & Kashmir",
        "Jammu and Kashmir"
    ])
)

if jk_mask.any():
    jk_index = india_states.index[
        jk_mask
    ][0]

    jk_geometry = india_states.loc[
        jk_index,
        "geometry"
    ]

    if isinstance(
        jk_geometry,
        MultiPolygon
    ):
        polygon_parts = list(
            jk_geometry.geoms
        )

        largest_area = max(

            polygon.area
            for polygon in polygon_parts
        )

        meaningful_polygons = [
            polygon
            for polygon in polygon_parts
            if polygon.area >= largest_area * 0.01
        ]

        if len(meaningful_polygons) == 1:

            cleaned_geometry = (
                meaningful_polygons[0]
            )

        else:
            cleaned_geometry = (
                MultiPolygon(
                    meaningful_polygons
                )
            )

        india_states.loc[
            jk_index,
            "geometry"
        ] = cleaned_geometry

        print(
            "Jammu & Kashmir geometry cleaned successfully."
        )
    else:
        print(
            "Jammu & Kashmir does not require MultiPolygon cleaning."
        )

else:
    print(
        "WARNING: Jammu & Kashmir was not found."
    )

# ============================================================
# 29.11 — KEEP REQUIRED COLUMNS
# ============================================================

india_states = india_states[
    [
        "ST_NM",
        "ST_ID",
        "ID",
        "geometry"
    ]
]

# ============================================================
# 29.12 — SAVE CLEAN SHAPEFILE
# ============================================================

india_states.to_file(

    OUTPUT_SHP,
    driver="ESRI Shapefile"
)

# ============================================================
# 29.13 — SAVE CLEAN GEOJSON
# ============================================================

india_states.to_file(

    OUTPUT_GEOJSON,
    driver="GeoJSON"
)

# ============================================================
# 29.14 — FINAL VERIFICATION
# ============================================================

print(
    "\nConversion completed successfully!"
)

print(
    "\nOriginal features:"
)

print(
    len(shp)
)

print(
    "\nFinal features:"
)

print(
    len(india_states)
)

print(
    "\nUnique States / UTs:"
)

print(
    india_states["ST_NM"].nunique()
)

print(
    "\nFinal columns:"
)

print(
    list(india_states.columns)
)

print(
    "\nClean Shapefile created:"
)

print(
    OUTPUT_SHP
)

print(
    "\nGeoJSON created:"
)

print(
    OUTPUT_GEOJSON
)