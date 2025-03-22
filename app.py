from pathlib import Path
import datetime

import pandas as pd
import streamlit as st

from src.perfs_tracker import PerfOfAllTime, MainPerf, SubPerf
from src.time_an_pace import Time


@st.cache_data
def load_data() -> PerfOfAllTime:
    filepath = Path("data/perfs.json")
    perfs = PerfOfAllTime()
    if filepath.exists():
        perfs.load_from_json(Path("data/perfs.json"))

    return perfs


if "perfs" not in st.session_state:
    perfs = load_data()
    st.session_state["perfs"] = perfs
    st.session_state["df"] = perfs.table()


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
df = st.session_state["df"]

st.sidebar.header("Filters")
df = filter_location(df)
df = filter_distance(df)
st.sidebar.subheader("Display performances")
st.write("Here are your best performances:")

st.dataframe(df, hide_index=True, use_container_width=True)


# Bouton pour afficher le formulaire
if "show_form" not in st.session_state:
    st.session_state["show_form"] = False

if st.button("➕ Ajouter une course"):
    st.session_state["show_form"] = not st.session_state["show_form"]

# Afficher le formulaire si activé
if st.session_state["show_form"]:
    with st.form(key="add_course_form"):
        new_name = st.text_input(
            "Nom de la course", placeholder="Ex: Marathon de Paris"
        )
        new_location = st.text_input("Ville", placeholder="Ex: Montpellier")

        col1, col2, col3 = st.columns(3)
        with col1:
            chrono_hours = st.number_input(
                "Heures", min_value=0, max_value=23, value=0, step=1
            )
        with col2:
            chrono_minutes = st.number_input(
                "Minutes", min_value=0, max_value=59, value=0, step=1
            )
        with col3:
            chrono_seconds = st.number_input(
                "Secondes", min_value=0, max_value=59, value=0, step=1
            )

        new_distance = st.number_input(
            "Distance (km)", min_value=0.1, max_value=500.0, value=10.0, step=0.1
        )

        submit_button = st.form_submit_button(label="✅ Ajouter la course")

        if submit_button:
            # Ajouter la nouvelle course au DataFrame de session_state
            new_time = Time(
                hours=chrono_hours, minutes=chrono_minutes, seconds=chrono_seconds
            )
            new_perf = MainPerf(
                name_event=new_name,
                date=datetime.datetime.now(),
                distance=new_distance,
                time=new_time,
                location=new_location,
            )
            print(new_perf)
            perfs: PerfOfAllTime = st.session_state["perfs"]
            perfs.add_perf(new_perf)
            st.session_state["df"] = perfs.table()

            # Sauvegarde des nouvelles données si on veut persister (désactivée pour éviter les rechargements)
            if perfs:
                perfs.save_to_json(Path("data/perfs.json"))

            st.success("✅ Course ajoutée avec succès !")

            # Masquer le formulaire après ajout
            st.session_state["show_form"] = False
            st.rerun()
