# ============================================================
# 27.17 — ACCURATE INDIA MAP TEST
# ============================================================

import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

from pathlib import Path

# ============================================================
# 27.17.02 — PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

GEOJSON_FILE = (
    PROJECT_DIR
    / "geojson"
    / "india.geojson"
)


# ============================================================
# 27.17.03 — LOAD GEOJSON
# ============================================================

with open(
    GEOJSON_FILE,
    encoding="utf-8"
) as file:

    india_geo = json.load(file)


# ============================================================
# 27.17.04 — EXTRACT STATE INFORMATION
# ============================================================

map_data = []

for feature in india_geo["features"]:

    state_name = feature["properties"].get("ST_NM")

    if state_name:

        map_data.append(
            {
                "state": state_name,
                "value": 1
            }
        )


map_df = pd.DataFrame(map_data)


# ============================================================
# 27.17.05 — PAGE HEADER
# ============================================================

st.title("🇮🇳 India Map Accuracy Test")

st.write(
    "Testing the complete India boundary and "
    "state borders before integration into IDIP."
)


# ============================================================
# 27.17.06 — CREATE FIGURE
# ============================================================

fig = go.Figure()


# ============================================================
# 27.17.07 — ADD INDIA STATE BOUNDARIES
# ============================================================

fig.add_trace(

    go.Choropleth(

        geojson=india_geo,

        locations=map_df["state"],

        featureidkey="properties.ST_NM",

        z=map_df["value"],

        colorscale=[
            [0, "rgba(0,0,0,0)"],
            [1, "rgba(0,0,0,0)"]
        ],

        showscale=False,

        marker=dict(
            line=dict(
                color="#7DD3FC",
                width=1.4
            )
        ),

        hovertemplate=(
            "<b>%{location}</b>"
            "<extra></extra>"
        )
    )
)


# ============================================================
# 27.17.08 — INDIA GEOGRAPHIC VIEW
# ============================================================

fig.update_geos(

    visible=False,

    projection_type="mercator",

    lonaxis_range=[
        67,
        99
    ],

    lataxis_range=[
        5,
        38
    ],

    showcoastlines=False,

    showcountries=False,

    showland=False,

    showocean=False,

    showlakes=False,

    showframe=False,

    bgcolor="#0E1117"
)


# ============================================================
# 27.17.09 — MAP LAYOUT
# ============================================================

fig.update_layout(

    height=750,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0
    ),

    paper_bgcolor="#0E1117",

    plot_bgcolor="#0E1117",

    dragmode=False
)


# ============================================================
# 27.17.10 — DISPLAY MAP
# ============================================================

st.plotly_chart(

    fig,

    width="stretch",

    config={
        "displayModeBar": False,
        "scrollZoom": False
    }
)