# ============================================================
# STATE INTELLIGENCE ENGINE
# ============================================================

import pandas as pd

# ============================================================
# MAIN FUNCTION
# ============================================================

def get_complete_state_intelligence(
    data,
    selected_state
):

    """
    Generates complete analytical intelligence
    for selected Indian state.

    Input:
        data -> output of load_idip_data()
        selected_state -> selected state name

    Output:
        dictionary containing:
        summary
        earthquake
        flood
        cyclone
        ml
        analysis_text
    """

    # ========================================================
    # LOAD DATASETS FROM DATA LOADER
    # ========================================================

    earthquake_df = data["earthquake"]
    flood_df = data["flood"]
    cyclone_df = data["cyclone"]
    state_disaster_df = data["state_disaster"]
    ml_state_summary_df = data["ml_state_summary"]

    # ========================================================
    # FILTER SELECTED STATE DATA
    # ========================================================

    earthquake_state = earthquake_df[
        earthquake_df["state_name"]
        == selected_state
    ].copy()

    flood_state = flood_df[
        flood_df["state_name"]
        == selected_state
    ].copy()


    cyclone_state = cyclone_df[
        cyclone_df["state_name"]
        == selected_state
    ].copy()

    # ========================================================
    # EVENT COUNTS
    # ========================================================

    earthquake_events = len(
        earthquake_state
    )

    flood_events = len(
        flood_state
    )

    cyclone_events = len(
        cyclone_state
    )

    total_events = (
        earthquake_events
        +
        flood_events
        +
        cyclone_events
    )

    # ========================================================
    # DOMINANT DISASTER
    # ========================================================

    disaster_count = {

        "Earthquake":
        earthquake_events,

        "Flood":
        flood_events,

        "Cyclone":
        cyclone_events

    }

    dominant_disaster = max(
        disaster_count,
        key=disaster_count.get
    )

    # ========================================================
    # EARTHQUAKE ANALYSIS
    # ========================================================

    if earthquake_events > 0:

        average_magnitude = round(
            pd.to_numeric(
                earthquake_state["magnitude"],
                errors="coerce"
            ).mean(),
            2
        )

        maximum_magnitude = round(
            pd.to_numeric(
                earthquake_state["magnitude"],
                errors="coerce"
            ).max(),
            2
        )

    else:

        average_magnitude = 0
        maximum_magnitude = 0

    earthquake = {

        "events":
        earthquake_events,

        "average_magnitude":
        average_magnitude,

        "maximum_magnitude":
        maximum_magnitude,

        "data":
        earthquake_state
    }

    # ========================================================
    # FLOOD ANALYSIS
    # ========================================================

    if flood_events > 0:

        total_fatalities = int(
            pd.to_numeric(
                flood_state["fatalities"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

        average_duration = round(
            pd.to_numeric(
                flood_state["duration_days"],
                errors="coerce"
            )
            .mean(),
            2
        )

    else:

        total_fatalities = 0
        average_duration = 0

    flood = {

        "events":
        flood_events,

        "total_fatalities":
        total_fatalities,

        "average_duration":
        average_duration,

        "data":
        flood_state
    }

    # ========================================================
    # CYCLONE ANALYSIS
    # ========================================================

    if cyclone_events > 0:

        maximum_wind_speed = round(
            pd.to_numeric(
                cyclone_state["wind_speed_knots"],
                errors="coerce"
            )
            .max(),
            2
        )

        minimum_pressure = round(
            pd.to_numeric(
                cyclone_state["pressure_mb"],
                errors="coerce"
            )
            .min(),
            2
        )

    else:
        maximum_wind_speed = 0
        minimum_pressure = 0

    cyclone = {
        "events":
        cyclone_events,

        "maximum_wind_speed":
        maximum_wind_speed,

        "minimum_pressure":
        minimum_pressure,

        "data":
        cyclone_state
    }

    # ========================================================
    # ML INTELLIGENCE
    # ========================================================

    ml_state = ml_state_summary_df[
        ml_state_summary_df[
            "nearest_indian_state"
        ]
        ==
        selected_state
    ]

    if not ml_state.empty:
        ml_row = (
            ml_state
            .iloc[0]
        )

        ml = {

            "available":
            True,

            "anomaly_candidates":
            ml_row["anomaly_candidates"],

            "closest_event_km":
            ml_row["closest_event_km"],

            "strongest_anomaly":
            ml_row["strongest_anomaly"],

            "highest_magnitude":
            ml_row["highest_magnitude"]
        }

    else:

        ml = {
            "available":
            False,

            "anomaly_candidates":
            0,

            "closest_event_km":
            None,
            "strongest_anomaly":
            None,
            "highest_magnitude":
            None
        }

    # ========================================================
    # ANALYTICAL WORDING
    # ========================================================

    analysis_text = (

        f"{selected_state} has recorded "
        f"{total_events} disaster events "
        f"across available historical datasets. "
        f"The dominant disaster category is "
        f"{dominant_disaster}. "
        f"Earthquake records: {earthquake_events}, "
        f"Flood records: {flood_events}, "
        f"Cyclone records: {cyclone_events}."

    )

    # ========================================================
    # FINAL RETURN STRUCTURE
    # ========================================================

    return {

        "summary": {

            "total_events":
            total_events,

            "dominant_disaster":
            dominant_disaster,

            "earthquake_events":
            earthquake_events,

            "flood_events":
            flood_events,

            "cyclone_events":
            cyclone_events

        },

        "earthquake":
        earthquake,

        "flood":
        flood,

        "cyclone":
        cyclone,

        "ml":
        ml,

        "analysis_text":
        analysis_text
    }