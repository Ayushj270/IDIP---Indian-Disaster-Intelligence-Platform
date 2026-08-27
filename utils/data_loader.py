from pathlib import Path
import pandas as pd
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    PROJECT_DIR
    / "all data"
    / "final_data"
)


# ============================================================
# LOAD IDIP DATA
# ============================================================

@st.cache_data
def load_idip_data():

    earthquake = pd.read_csv(
        DATA_DIR / "earthquake_final.csv"
    )

    flood = pd.read_csv(
        DATA_DIR / "flood_final.csv"
    )

    cyclone = pd.read_csv(
        DATA_DIR / "cyclone_final.csv"
    )

    state_disaster = pd.read_csv(
        DATA_DIR / "state_disaster_summary.csv"
    )

    ml_output = pd.read_csv(
        DATA_DIR / "earthquake_ml_output.csv"
    )

    ml_state_summary = pd.read_csv(
        DATA_DIR / "earthquake_ml_state_summary.csv"
    )

    return {
        "earthquake": earthquake,
        "flood": flood,
        "cyclone": cyclone,
        "state_disaster": state_disaster,
        "ml_output": ml_output,
        "ml_state_summary": ml_state_summary
    }