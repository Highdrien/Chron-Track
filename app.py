from pathlib import Path

import pandas as pd
import streamlit as st

from src.perfs_tracker import PerfOfAllTime


def load_data() -> PerfOfAllTime:
    filepath = Path("data/perfs.json")
    perfs = PerfOfAllTime()
    if filepath.exists():
        perfs.load_from_json(Path("data/perfs.json"))

    return perfs


def filter_location(df: pd.DataFrame) -> pd.DataFrame:
    locations = df["Location"].unique()
    locations.sort()
    selected_location = st.sidebar.selectbox(
        "Filter by location :", ["All"] + list(locations)
    )
    if selected_location != "All":
        df = df[df["Location"] == selected_location]

    return df


def filter_distance(df: pd.DataFrame) -> pd.DataFrame:
    distances = df["Distance (km)"].unique()
    distances.sort()
    selected_distance = st.sidebar.selectbox(
        "Filter by distance (km) :", ["All"] + list(distances)
    )
    if selected_distance != "All":
        df = df[df["Distance (km)"] == selected_distance]

    return df


st.title("Performances of All Time")
st.write("This app allows you to track your performances over time.")
perfs = load_data()
df = perfs.table()

st.sidebar.header("Filters")
df = filter_location(df)
df = filter_distance(df)


st.dataframe(df, hide_index=True, use_container_width=True)
