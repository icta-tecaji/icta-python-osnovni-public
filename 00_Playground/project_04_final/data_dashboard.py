from __future__ import annotations

import httpx
import pandas as pd
import streamlit as st

BASE_URL = "http://localhost:8000"


@st.cache_data
def fetch_meritve_data(limit: int = 500) -> pd.DataFrame:
    """Fetch the data from the API."""
    params = {
        "start_timestamp": 0,
        "limit": limit,
    }
    response = httpx.get(f"{BASE_URL}/meritve", params=params)
    data = response.json()
    data_df = pd.DataFrame(data["meritve"])
    return data_df


# --------------------------------- APP --------------------------------- #
st.title("# Aplikacija za analizo meritev")

max_data_limit = st.number_input("Omejitev števila podatkovnih točk", value=500, min_value=100, max_value=100_000)
st.write(f"Omejitev števila podatkovnih točk: {max_data_limit}")

data = fetch_meritve_data(int(max_data_limit))

### PRIKAZ GRAFOV
st.write(f"Število podatkovnih točk: {data.shape[0]}")
st.write("### NTC temperatura")
st.line_chart(
    data=data,
    x="timestamp",
    y=["ntc_temp", "bridge_temp"],
    y_label="NTC temperatura (°C)",
    x_label="Miliseconds from time",
    color=["#5234eb", "#eb3434"],
)

st.write("### RPM speed")
st.line_chart(
    data=data,
    x="timestamp",
    y=["target_speed_rpm", "speed_rpm"],
    y_label="RPM speed",
    x_label="Miliseconds from time",
    color=["#34eb52", "#eb5234"],
)

st.write("### Motor power")
st.line_chart(
    data=data,
    x="timestamp",
    y=["motor_power_w"],
    y_label="Motor power (W)",
    x_label="Miliseconds from time",
    color=["#34eb52"],
)
