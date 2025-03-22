from pathlib import Path
import datetime

import pandas as pd
import streamlit as st

from src.perfs_tracker import PerfOfAllTime, MainPerf
from src.time_an_pace import Time


@st.cache_data
def load_data() -> PerfOfAllTime:
    """
    Loads performance data from a JSON file.
    """
    filepath = Path("data/perfs.json")
    perfs = PerfOfAllTime()
    if filepath.exists():
        perfs.load_from_json(Path("data/perfs.json"))

    return perfs


def filter_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the given DataFrame by a selected location using
    a Streamlit sidebar selectbox.

    Args:
        df (pd.DataFrame): The input DataFrame containing a "Location" column.

    Returns:
        pd.DataFrame: The filtered DataFrame based on the selected location.
            If "All" is selected, the original DataFrame is returned.
    """
    locations = df["Location"].unique()
    locations.sort()
    selected_location = st.sidebar.selectbox(
        "Filter by location :", ["All"] + list(locations)
    )
    if selected_location != "All":
        df = df[df["Location"] == selected_location]

    return df


def filter_distance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the given DataFrame based on the selected distance from a Streamlit sidebar.

    Args:
        df (pd.DataFrame): The input DataFrame containing a column "Distance (km)".

    Returns:
        pd.DataFrame: The filtered DataFrame based on the selected distance.
    """
    distances = df["Distance (km)"].unique()
    distances.sort()
    selected_distance = st.sidebar.selectbox(
        "Filter by distance (km) :", ["All"] + list(distances)
    )
    if selected_distance != "All":
        df = df[df["Distance (km)"] == selected_distance]

    return df


def add_new_race():
    """
    Displays a form to add a new race event with details such as name, location, time,
    and distance. On form submission, the new race is added to the session state
    DataFrame and saved to a JSON file.
    """
    new_name = st.text_input("Nom de la course", placeholder="Ex: Marathon de Paris")
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

        if perfs:
            perfs.save_to_json(Path("data/perfs.json"))

        st.success("✅ Course ajoutée avec succès !")

        # Masquer le formulaire après ajout
        st.session_state["show_form"] = False
        st.rerun()
