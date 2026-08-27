# ============================================================
# 27.01 — IMPORT LIBRARIES
# ============================================================

import streamlit as st

st.set_page_config(
    page_title="IDIP",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from utils.data_loader import load_idip_data
from utils.state_page import (
    show_state_intelligence_page
)
from utils.india_map import (
    load_india_geojson,
    get_india_states,
    create_india_map,
    create_state_uplift_map
)
from utils.graph_intelligence import (
    get_complete_graph_intelligence
)

# ============================================================
# 27.02 — PAGE CONFIGURATION
# ============================================================

# ============================================================
# 27.03 — LOAD DATA
# ============================================================

data = load_idip_data()

# ============================================================
# 27.04 — LOAD INDIA MAP
# ============================================================

india_geo = load_india_geojson()
states = get_india_states(
    india_geo
)
# ============================================================
# 27.05 — INITIALIZE SESSION STATE
# ============================================================

if "selected_state" not in st.session_state:
    st.session_state["selected_state"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "state_view" not in st.session_state:
    st.session_state["state_view"] = "analysis"

# ============================================================
# 27.06 — PAGE ROUTING
# ============================================================

if st.session_state["page"] == "state_intelligence":
    selected_state = st.session_state.get(
        "selected_state"
    )
    if selected_state is not None:
        show_state_intelligence_page(
            selected_state=selected_state,
            data=data,
            india_geo=india_geo
        )
        st.stop()

# ============================================================
# 27.07 — HOME PAGE HEADER
# ============================================================

st.title(
    "🌍 IDIP"
)

st.subheader(
    "Natural Disaster Intelligence & Management"
)

st.divider()

# ============================================================
# 27.08 — STATE SELECTION TITLE
# ============================================================

st.markdown(
    """
    <h2 style="
        text-align:center;
        margin-top:10px;
        margin-bottom:20px;
    ">
        Select a State to Explore
    </h2>
    """,
    unsafe_allow_html=True
)
# ============================================================
# 27.09 — STATE SELECTOR
# ============================================================

left_col, center_col, right_col = st.columns(
    [1,1.2,1]
)
with center_col:
    selected_state = st.selectbox(
        "Select a State",
        options=[
            "Select a State"
        ] + states,
        label_visibility="collapsed"
    )

# ============================================================
# 27.10 — STORE SELECTED STATE
# ============================================================

if selected_state == "Select a State":
    current_selected_state = None

else:
    current_selected_state = selected_state

# ============================================================
# 27.11 — INDIA MAP
# ============================================================

fig = create_india_map(
    india_geo=india_geo,
    states=states,
    selected_state=current_selected_state
)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "displayModeBar":False,
        "scrollZoom":False
    }
)

# ============================================================
# 27.12 — SELECTED STATE UPLIFT MAP
# ============================================================

if current_selected_state:

    uplift_fig = create_state_uplift_map(
        india_geo=india_geo,
        selected_state=current_selected_state
    )

    if uplift_fig is not None:

        left, middle, right = st.columns(
            [1,1.5,1]
        )

        with middle:

            st.plotly_chart(
                uplift_fig,
                width="stretch",
                config={
                    "displayModeBar":False,
                    "scrollZoom":False
                }
            )

# ============================================================
# 27.13 — EXPLORE STATE BUTTON
# ============================================================

if current_selected_state:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1.5,1,1.5]
    )
    with center:

        if st.button(

            f"Explore {current_selected_state} →",
            type="primary"

        ):
            # SAVE STATE HERE
            st.session_state[
                "selected_state"
            ] = current_selected_state

            # MOVE TO STATE PAGE
            st.session_state[
                "page"
            ] = "state_intelligence"

            st.rerun()