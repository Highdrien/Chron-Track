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
locations = df["location"].unique()

# Ajouter une option "Tous" pour afficher toutes les courses
selected_location = st.selectbox("Filtrer par ville :", ["Tous"] + list(locations))

# Filtrer le DataFrame si une ville est sélectionnée (sauf "Tous")
if selected_location != "Tous":
    df = df[df["location"] == selected_location]

st.dataframe(df, hide_index=True, use_container_width=True)
