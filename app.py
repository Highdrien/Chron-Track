import streamlit as st
from pathlib import Path

from src.perfs_tracker import PerfOfAllTime


def load_data() -> PerfOfAllTime:
    filepath = Path("data/perfs.json")
    perfs = PerfOfAllTime()
    if filepath.exists():
        perfs.load_from_json(Path("data/perfs.json"))

    return perfs


st.title("Performances of All Time")
st.write("This app allows you to track your performances over time.")
perfs = load_data()
df = perfs.table()

st.sidebar.header("Filters")

# Filter by location
locations = df["location"].unique()
locations.sort()
selected_location = st.sidebar.selectbox(
    "Filter by location :", ["All"] + list(locations)
)
if selected_location != "All":
    df = df[df["location"] == selected_location]

# Filter by distance
distances = df["distance"].unique()
distances.sort()
selected_distance = st.sidebar.selectbox(
    "Filter by distance (km) :", ["All"] + list(distances)
)
if selected_distance != "All":
    df = df[df["distance"] == selected_distance]

st.dataframe(df, hide_index=True, use_container_width=True)
